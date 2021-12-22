#!/usr/bin/env python3
import time, itertools, functools, re
import numpy as np
from io import StringIO
from collections import Counter, defaultdict
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, **kwargs):
        return iterable

def part1(cmds):
    grid = np.zeros((101, 101, 101), dtype=bool)
    for cmd, coords in cmds:
        grid[coords[0][0]+50:coords[0][1]+51,
             coords[1][0]+50:coords[1][1]+51,
             coords[2][0]+50:coords[2][1]+51] = cmd == 'on'
    return grid.sum()

def contains(c1, c2) -> bool:
    """check if c1 contains c2 (total overlap)"""
    return (c2[0][0] >= c1[0][0] and c2[0][1] <= c1[0][1] and
            c2[1][0] >= c1[1][0] and c2[1][1] <= c1[1][1] and
            c2[2][0] >= c1[2][0] and c2[2][1] <= c1[2][1])

def overlaps(c1, c2) -> bool:
    """check if c1 overlaps c2 (any overlap)"""
    return not (c1[0][1] <= c2[0][0] or c2[0][1] <= c1[0][0] or
                c1[1][1] <= c2[1][0] or c2[1][1] <= c1[1][0] or
                c1[2][1] <= c2[2][0] or c2[2][1] <= c1[2][0])

def get_overlap(c1, c2):
    assert not (contains(c1, c2) or contains(c2, c1))
    if not overlaps(c1, c2):
        return None
    if c2[0][0] < c1[0][1]:
        x = (c2[0][0], c1[0][1])
    else:
        x = (c1[0][0], c2[0][1])

    if c2[1][0] < c1[1][1]:
        y = (c2[1][0], c1[1][1])
    else:
        y = (c1[1][0], c2[1][1])

    if c2[2][0] < c1[2][1]:
        z = (c2[2][0], c1[2][1])
    else:
        z = (c1[2][0], c2[2][1])

    return (x, y, z)

def part2(cmds):
    """
        cuboids = set()  # each entry is non-overlapping region turned ON
        for each cmd, newblock:
            if ON:
                for c in cuboid:
                    if newblock overlaps c:
                        fracture newblock into cuboids along c boundaries
                        eliminate subblock completely overlapped by c
                        add remaining subblocks to cuboids  # note they may overlap cuboids
            if OFF:
                for c in cuboid:
                    if newblock overlaps c:
                        remove c from cuboids
                        fracture c into cuboids along newblock boundaries
                        eliminate subblock completely overlapped by c
                        add remaining subblocks to cuboids  # note they may overlap cuboids

            while cuboids
                for each pair c1, c2 in cuboids:
                    if c1 completely overlaps c2:
                        remove c2 from cuboids
                    else if c2 completely overlaps c1:
                        remove c1 from cuboids
                for each pair c1, c2 in cuboids:
                    if c1 overlaps c2:
                        fracture c2 into cuboids along c1 boundaries
                        eliminate subblock completely overlapped by c1
                        add remaining subblocks to cuboids  # note they may overlap cuboids
        return sum of volumes of cuboids
    """

    # redefine cuboids by their min 3-coord and size: ((x, y, z), (|x|, |y|, |z|))
    # ((c[0][0], c[1][0], c[2][0]), (c[0][1]-c[0][0]+1, c[0][1]-c[0][0]+1, c[0][1]-c[0][0]+1))
    # cuboids = []
    # for cmd, c in cmds:
    #     pass

    c1 = ((0, 3), (0, 3), (0, 3))
    c2 = ((4, 5), (4, 5), (4, 5))
    c3 = ((1, 2), (1, 2), (1, 2))
    c4 = ((2, 4), (2, 4), (2, 4))
    c5 = ((-2, 1), (-2, 1), (-2, 1))
    print(c1)
    print(c5)
    print(get_overlap(c1, c5))
    print(get_overlap(c5, c1))
    # print(overlaps(c1, c2))
    # print(overlaps(c2, c1))
    # print(overlaps(c1, c3))
    # print(overlaps(c3, c1))
    # print(contains(c1, c3))
    # print(contains(c3, c1))

def parse_input(data_src):
    data_src.seek(0)
    cmds = []
    for line in data_src:
        cmd = line.split()
        axes = cmd[1].split(',')
        cmds.append((cmd[0], tuple([tuple(map(int, axes[x].split('=')[1].split('..'))) for x in range(3)])))
    return cmds

def run_tests():
    TEST_INPUT = """
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""
    test_data = StringIO(TEST_INPUT.strip())
    assert part1(parse_input(test_data)) == 474140
    assert part2(parse_input(test_data)) == 2758514936282235

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    # with open(__file__[:-3] + '-input.dat') as infile:
    #     print_result('1', part1, parse_input(infile))  # 598616
    #     print_result('2', part2, parse_input(infile))  # -
