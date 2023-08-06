import numpy as np
import sigpy as sp


# Gyromagnetic ratios in rad / (s G)
proton_gamma = 26751.3


def p0(ishape=[], dtype=np.complex, device=sp.cpu_device):
    xp = device.xp
    p0 = xp.zeros(list(ishape) + [2, 2], dtype=dtype, device=device)
    with device:
        p0[..., 0, 0] = 1

    return p0


def get_mx(p):

    return (p[..., 1, 0] + p[..., 0, 1]).real


def get_my(p):
    
    return (-1j * p[..., 1, 0] + 1j * p[..., 0, 1]).real


def get_mz(p):
    
    return (p[..., 0, 0] - p[..., 1, 1]).real


def m_to_p(mx, my, mz):

    ishape = list(mx.shape)
    device = sp.get_device(mx)
    xp = device.xp
    
    p = xp.zeros(ishape + [2, 2], dtype=np.complex, device=device)
    with device:
        p[..., 0, 0] = (1 + mz) / 2
        p[..., 1, 0] = (mx + 1j * my) / 2
        p[..., 0, 1] = (mx - 1j * my) / 2
        p[..., 1, 1] = (1 - mz) / 2

    return p


def rot_mat(b1, dt, gamma=proton_gamma):

    device = sp.get_device(b1)
    xp = device.xp

    with device:
        alpha = xp.abs(b1) * dt * gamma
        phi = xp.angle(b1)
        
        cos_alpha = xp.cos(alpha / 2)
        sin_alpha = xp.sin(alpha / 2)
        cos_phi = xp.cos(phi)
        sin_phi = xp.sin(phi)

        if xp.isscalar(b1):
            r = xp.zeros([2, 2], dtype=np.complex, device=device)
        else:
            r = xp.zeros(list(b1.shape) + [2, 2], dtype=np.complex, device=device)

        r[..., 0, 0] = cos_alpha
        r[..., 1, 0] = -1j * sin_alpha * cos_phi + sin_alpha * sin_phi
        r[..., 0, 1] = -1j * sin_alpha * cos_phi - sin_alpha * sin_phi
        r[..., 1, 1] = cos_alpha

    return r


def hard_pulse(p, r):
    device = sp.get_device(p)
    xp = device.xp

    with device:
        p = r @ p @ xp.conj(r).swapaxes(-1, -2)
        
        return p


def hard_pulse_adjoint(p, r):
    device = sp.get_device(p)
    xp = device.xp

    with device:
        p = xp.conj(r).swapaxes(-1, -2) @ p @ r
        return p


def fid(p, f0, r1, r2, dt):
    device = sp.get_device(p)
    xp = device.xp

    with device:
        e2 = xp.exp(-dt * r2)
        e1 = xp.exp(-dt * r1)
        e0 = xp.exp(-1j * dt * 2 * np.pi * f0)

        p = p.copy()
        p[..., 0, 0] *= e1
        p[..., 1, 1] *= e1
        p[..., 1, 0] *= e0 * e2
        p[..., 0, 1] *= xp.conj(e0) * e2
        
        p[..., 0, 0] += 1 - e1

    return p


def fid_adjoint(p, f0, r1, r2, dt):
    device = sp.get_device(p)
    xp = device.xp

    with device:
        e2 = xp.exp(-dt * r2)
        e1 = xp.exp(-dt * r1)
        e0 = xp.exp(-1j * dt * 2 * np.pi * f0)

        p = p.copy()
        p[..., 0, 0] *= e1
        p[..., 1, 1] *= e1
        p[..., 1, 0] *= xp.conj(e0) * e2
        p[..., 0, 1] *= e0 * e2

    return p


def bloch_forward(p0, b1s, f0, r1, r2, dt, gamma=proton_gamma):
    """Bloch equation in density matrix representation.
    
    Args:
        p0 (array): initial density matrix, ishape + [2, 2]
        b1s (array): b1 array, G, [N]
        f0 (array): off resonance frequency, ishape, or scalar
        r1 (array): R1 recovery, ishape, or scalar
        r2 (array): R2 decay, ishape or scalar
        dt (scalar): delta time, s, scalar
        gamma (scalar): gyromagnetic ratio, rad / s / G

    Returns:
        array: resulting density matrix, ishape + [2, 2]

    """
    p = p0
    rs = rot_mat(b1s, dt, gamma=gamma)
    for r in rs:
        p = fid(p, f0, r1, r2, dt)
        p = hard_pulse(p, r)

    return p


def lie_bracket(a, b):

    return a @ b - b @ a


def bloch_gradient(y, W, p0, b1s, f0, r1, r2, dt, gamma=proton_gamma):
    """
    Gradient of Bloch equation w.r.t. b1s.
    
    y - desired density matrix, ishape + [2, 2]
    W - weights
    p0 - initial density matrix, ishape + [2, 2]
    b1s - b1 array, G, [N]
    f0 - off resonance frequency, ishape, or scalar
    r1 - R1 recovery, ishape, or scalar
    r2 - R2 decay, ishape or scalar
    dt - delta time, s, scalar
    gamma - gyromagnetic ratio, rad / s / G

    Returns
    gs - gradient, [N]
    """
    
    device = sp.get_device(p0)
    xp = device.xp

    with device:
        # forward
        ps = []
        p = p0
        rs = rot_mat(b1s, dt, gamma=gamma)
        for r in rs:
            p = fid(p, f0, r1, r2, dt)
            p = hard_pulse(p, r)
            ps.append(p)

        Ix = xp.array([[0, 1],
                       [1, 0]], np.complex)

        Iy = xp.array([[0, -1j],
                       [1j, 0]], np.complex)

        # adjoint
        gs = []
        l = W * (p - y)
        for r, p in zip(rs[::-1], ps[::-1]):
            gr = xp.real(xp.vdot(l, -1j * gamma * dt * lie_bracket(Ix, p)))
            gi = xp.real(xp.vdot(l, -1j * gamma * dt * lie_bracket(Iy, p)))

            gs = [gr + 1j * gi] + gs

            l = hard_pulse_adjoint(l, r)
            l = fid_adjoint(l, f0, r1, r2, dt)
            
        return xp.stack(gs, axis=0)
