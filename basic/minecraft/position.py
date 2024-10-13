""" Minecraft position calculator """


def get_chunk_from_pos(pos_x: int, pos_z: int) -> (int, int):
    c_x = int(pos_x / 16) if pos_x >= 0 else int((pos_x-1) / 16)-1
    c_z = int(pos_z / 16) if pos_z >= 0 else int((pos_z-1) / 16)-1

    return c_x, c_z


def get_region_from_chunk(chunk_x: int, chunk_z: int) -> (int, int):
    r_x = int(chunk_x / 32) if chunk_x >= 0 else int((chunk_x+1) / 32)-1
    r_z = int(chunk_z / 32) if chunk_z >= 0 else int((chunk_z+1) / 32)-1

    return r_x, r_z


def get_chunk_relative_position(chunk_x: int, chunk_z: int) -> (int, int):
    r_x, r_z = get_region_from_chunk(chunk_x, chunk_z)
    relative_x_0 = r_x * 32
    relative_z_0 = r_z * 32
    relative_x = abs(relative_x_0) - abs(chunk_x) if chunk_x < 0 else chunk_x - relative_x_0
    relative_z = abs(relative_z_0) - abs(chunk_z) if chunk_z < 0 else chunk_z - relative_z_0

    return relative_x, relative_z