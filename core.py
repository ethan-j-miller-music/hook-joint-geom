# Layer 0：四个函数实现（唯一实现源）



def direction_from_angles(theta_x, theta_y) -> n (3,)

def angles_from_direction(n, *, eps=1e-12, pole_theta_x=0.0) -> (theta_x, theta_y)

def rope_lengths_from_angles(theta_x, theta_y, *, r, h, phis) -> L (N,)

def rope_lengths_from_direction(n, *, r, h, phis, eps=1e-12, pole_theta_x=0.0) -> L (N,)
