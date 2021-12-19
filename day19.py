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

"""
90 deg rotation: x,y -> -y,x
when negating axis, swap un-negated axes to preserve handedness

a,b,c ->
    x,y,z     -x,z,y
    x,-z,y    -x,y,-z
    x,-y,-z   -x,-z,-y
    x,z,-y    -x,-y,z

    y,z,x     -y,x,z
    y,-x,z    -y,z,-x
    y,-z,-x   -y,-x,-z
    y,x,-z    -y,-z,x

    z,x,y     -z,y,x
    z,-y,x    -z,x,-y
    z,-x,-y   -z,-y,-x
    z,y,-x    -z,-x,y
"""

ORIENTATIONS = [
    (1,2,3), (1,-3,2), (1,-2,-3), (1,3,-2),
    (-1,3,2), (-1,2,-3), (-1,-3,-2), (-1,-2,3),
    (2,3,1), (2,-1,3), (2,-3,-1), (2,1,-3),
    (-2,1,3), (-2,3,-1), (-2,-1,-3), (-2,-3,1),
    (3,1,2), (3,-2,1), (3,-1,-2), (3,2,-1),
    (-3,2,1), (-3,1,-2), (-3,-2,-1), (-3,-1,2)
]

def reorient(coords, rho):
    sign = (rho[0]//abs(rho[0]), rho[1]//abs(rho[1]), rho[2]//abs(rho[2]))
    return [(c[abs(rho[0])-1]*sign[0],
             c[abs(rho[1])-1]*sign[1],
             c[abs(rho[2])-1]*sign[2]) for c in coords]

def find_alignment(A, B):
    def vecdiff(a, b):
        return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

    for a in A:
        # skip the first 11 coords in B (or A); if there's an alignment it
        # will still be found but if there isn't we can check fewer points
        for b in list(B)[11:]:
            shift = vecdiff(b, a)
            shifted = [vecdiff(c, shift) for c in B]
            overlap = [x for x in shifted if x in A]
            if len(overlap) >= 12:
                return shift, set(shifted)
    return None

def both_parts(scanners):
    solved = [0]
    unsolved = set(range(1, len(scanners)))
    locations = [(0, 0, 0)]
    with tqdm(total=len(scanners)-1, ncols=80, leave=False) as progress:
        while unsolved:
            idx_a = solved.pop(0)
            found = []
            for idx_b in unsolved:
                for rho in ORIENTATIONS:
                    oriented = reorient(scanners[idx_b], rho)
                    if shift := find_alignment(scanners[idx_a], oriented):
                        progress.update(1)
                        found.append(idx_b)
                        locations.append(shift[0])
                        scanners[idx_b] = shift[1]
            solved.extend(found)
            for idx in found:
                unsolved.remove(idx)


    part1 = len({b for beacons in scanners.values() for b in beacons})
    part2 = max(abs(np.array(a)-np.array(b)).sum()
                for a, b in itertools.combinations(locations, 2))
    return part1, part2

def parse_input(data_src):
    data_src.seek(0)
    scanners = defaultdict(set)
    for line in data_src:
        line = line.strip()
        if m := re.match(r'.*scanner (\d+).*', line):
            idx = int(m.groups()[0])
        elif line:
            scanners[idx].add(tuple(map(int, line.split(','))))
    return scanners

def run_tests():
    TEST_INPUT = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
    test_data = StringIO(TEST_INPUT.strip())
    answer = both_parts(parse_input(test_data))
    assert answer == (79, 3621)

def print_result(part_label, part_fn, *args):
    start = time.perf_counter()
    result = part_fn(*args)
    end = time.perf_counter()
    print(f"Part {part_label}: {result}  ({int((end-start)*1000)} ms)")

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        start = time.perf_counter()
        result = both_parts(parse_input(infile))
        end = time.perf_counter()
        print(f"Part 1: {result[0]}  ({int((end-start)*1000)} ms)")  # 330
        print(f"Part 2: {result[1]}  (0 ms)")  # 9634
