print("=" * 50)
print("TOWER OF HANOI")
print("=" * 50)

def display_towers(towers):
    print(f"Tower A: {towers['A']}")
    print(f"Tower B: {towers['B']}")
    print(f"Tower C: {towers['C']}")

def move_disk(towers, source, destination):
    source_tower = towers[source]
    dest_tower = towers[destination]

    if not source_tower:
        print(f"Invalid move! Tower {source} is empty.")
        return None
    disk = source_tower[-1]

    if dest_tower and dest_tower[-1] < disk:
        print("Invalid move! Cannot place larger disk on smaller disk.")
        return None
    disk = source_tower.pop()
    dest_tower.append(disk)
    return disk


while True:
    try:
        n = int(input("\nEnter the number of disks (1-8): "))
        if 1 <= n <= 8:
            break
        else:
            print("Please enter a number between 1 and 8!")
    except ValueError:
        print("Please enter a valid number!")


tower_A = list(range(n, 0, -1))
tower_B = []
tower_C = []

towers = {
    'A': tower_A,
    'B': tower_B,
    'C': tower_C
}

stack = [(n, 'A', 'C', 'B')]
move_count = 0

print(f"\nSolving Tower of Hanoi with {n} disks...")
print("Moving from Tower A to Tower C using Tower B as auxiliary")
print("\nInitial State:")
display_towers(towers)
print("\n" + "=" * 50)

while stack:
    disks, source, destination, auxiliary = stack.pop()
    if disks == 1:
        disk = move_disk(towers, source, destination)
        if disk is not None:
            move_count += 1

            print(
                f"Move {move_count}: Move disk {disk} "
                f"from Tower {source} to Tower {destination}"
            )
            display_towers(towers)
            print("-" * 50)

    else:
        stack.append((disks - 1, auxiliary, destination, source))
        stack.append((1, source, destination, auxiliary))
        stack.append((disks - 1, source, auxiliary, destination))

print("\n" + "=" * 50)
print("🎉 PUZZLE SOLVED!")
print(f"Total moves: {move_count}")
print(f"Minimum moves required: {2**n - 1}")
print("=" * 50)
