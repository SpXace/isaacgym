from isaacgym import gymapi
from isaacgym import gymutil
import random
 
 
 
def setup():
    args = gymutil.parse_arguments(
    description="mytest",
)
    gym = gymapi.acquire_gym()
    sim_params = gymapi.SimParams()
    # get default set of parameters
    sim_params = gymapi.SimParams()
 
    # set common parameters
    sim_params.dt = 1 / 60
    sim_params.substeps = 2
    sim_params.up_axis = gymapi.UP_AXIS_Z
    sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
 
    # set PhysX-specific parameters
    sim_params.physx.use_gpu = True
    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 6
    sim_params.physx.num_velocity_iterations = 1
    sim_params.physx.contact_offset = 0.01
    sim_params.physx.rest_offset = 0.0
 
    # set Flex-specific parameters
    sim_params.flex.solver_type = 5
    sim_params.flex.num_outer_iterations = 4
    sim_params.flex.num_inner_iterations = 20
    sim_params.flex.relaxation = 0.8
    sim_params.flex.warm_start = 0.5
    #set gravity
    sim_params.up_axis = gymapi.UP_AXIS_Z
    sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
 
 
 
    # create sim with these parameters
 
    sim = gym.create_sim(args.compute_device_id, args.graphics_device_id,gymapi.SIM_PHYSX, sim_params)
    # configure the ground plane
    plane_params = gymapi.PlaneParams()
    plane_params.normal = gymapi.Vec3(0, 0, 1) # z-up!
    plane_params.distance = 0
    plane_params.static_friction = 1
    plane_params.dynamic_friction = 1
    plane_params.restitution = 0
 
    # create the ground plane
    gym.add_ground(sim, plane_params)
    
    
    
    '''loading assets'''
    asset_root = "assets"
    asset_file = "urdf/franka_description/robots/franka_panda.urdf"
    asset_options = gymapi.AssetOptions()
    asset_options.fix_base_link = True
    asset_options.armature = 0.01
 
    asset = gym.load_asset(sim, asset_root, asset_file, asset_options)
    
    '''loading environment'''
    spacing = 2.0
    lower = gymapi.Vec3(-spacing, 0.0, -spacing)
    upper = gymapi.Vec3(spacing, spacing, spacing)
 
    env = gym.create_env(sim, lower, upper, 8)
    
    '''actors create'''
    pose = gymapi.Transform()
    pose.p = gymapi.Vec3(0.0, 1.0, 0.0)
    pose.r = gymapi.Quat(-0.707107, 0.0, 0.0, 0.707107)#四元数表示
    #pose.r = gymapi.Quat.from_axis_angle(gymapi.Vec3(1, 0, 0), -0.5 * math.pi)
    #这是表示绕x旋转-90度数
 
    actor_handle = gym.create_actor(env, asset, pose, "MyActor", 0, 1)#actor必须放在指定env中
 
def test():
    args = gymutil.parse_arguments(
    description="mytest",
)
    gym = gymapi.acquire_gym()
    sim_params = gymapi.SimParams()
    # get default set of parameters
    sim_params = gymapi.SimParams()
 
    # set common parameters
    sim_params.dt = 1 / 60
    sim_params.substeps = 2
    sim_params.up_axis = gymapi.UP_AXIS_Z
    sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
 
    # set PhysX-specific parameters
    sim_params.physx.use_gpu = True
    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 6
    sim_params.physx.num_velocity_iterations = 1
    sim_params.physx.contact_offset = 0.01
    sim_params.physx.rest_offset = 0.0
 
    # set Flex-specific parameters
    sim_params.flex.solver_type = 5
    sim_params.flex.num_outer_iterations = 4
    sim_params.flex.num_inner_iterations = 20
    sim_params.flex.relaxation = 0.8
    sim_params.flex.warm_start = 0.5
    #set gravity
    sim_params.up_axis = gymapi.UP_AXIS_Z
    sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
 
 
 
    # create sim with these parameters
 
    sim = gym.create_sim(args.compute_device_id, args.graphics_device_id,gymapi.SIM_PHYSX, sim_params)
    # configure the ground plane
    plane_params = gymapi.PlaneParams()
    plane_params.normal = gymapi.Vec3(0, 0, 1) # z-up!
    plane_params.distance = 0
    plane_params.static_friction = 1
    plane_params.dynamic_friction = 1
    plane_params.restitution = 0
 
    # create the ground plane
    gym.add_ground(sim, plane_params)
    
    
    
    '''loading assets'''
    asset_root = "assets"
    asset_file = "urdf/franka_description/robots/franka_panda.urdf"
    asset_options = gymapi.AssetOptions()
    asset_options.fix_base_link = True
    asset_options.armature = 0.01
 
    asset = gym.load_asset(sim, asset_root, asset_file, asset_options)
    # set up the env grid
    num_envs = 64
    envs_per_row = 8
    env_spacing = 2.0
    env_lower = gymapi.Vec3(-env_spacing, 0.0, -env_spacing)
    env_upper = gymapi.Vec3(env_spacing, env_spacing, env_spacing)
 
    # cache some common handles for later use
    envs = []
    actor_handles = []
 
    # create and populate the environments
    for i in range(num_envs):
        env = gym.create_env(sim, env_lower, env_upper, envs_per_row)
        envs.append(env)#envs的索引和actors的一致这样就可以防止actors跟别的env碰撞
 
        height = random.uniform(1.0, 2.5)
 
        pose = gymapi.Transform()
        pose.p = gymapi.Vec3(0.0, height, 0.0)
 
        actor_handle = gym.create_actor(env, asset, pose, "MyActor", i, 1)
        actor_handles.append(actor_handle)
        '''viewer create'''
        cam_props = gymapi.CameraProperties()
        viewer = gym.create_viewer(sim, cam_props)
        
        
        num=0
        while not gym.query_viewer_has_closed(viewer):
 
            # step the physics
            gym.simulate(sim)
            gym.fetch_results(sim, True)
 
            # update the viewer
            gym.step_graphics(sim)
            gym.draw_viewer(viewer, sim, True)
 
            # Wait for dt to elapse in real time.
            # This synchronizes the physics simulation with the rendering rate.
            gym.sync_frame_time(sim)
            num+=1
            if num>10:
                print(num)
            #gym.destroy_viewer(viewer)
                #gym.destroy_sim(sim)
 
 
    
 
 
 
if __name__ =='__main__':
    #setup()
    test()