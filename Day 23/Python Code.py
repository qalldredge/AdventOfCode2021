from functools import lru_cache

rooms_main = (("A", "D"), ("C", "D"), ("B", "A"), ("B", "C"))
rooms_example = (("B", "A"), ("C", "D"), ("B", "C"), ("D", "A"))

rooms_main2 = (("A", "D", "D", "D"), ("C", "C", "B", "D"), ("B", "B", "A", "A"), ("B", "A", "C", "C"))
rooms_example2 = (("B", "D", "D", "A"), ("C", "C", "B", "D"), ("B", "B", "A", "C"), ("D", "A", "C", "A"))


def main():
    print(f(rooms_example))
    print(f(rooms_main))

    print(f(rooms_example2))
    print(f(rooms_main2))


def f(lines):
    room_map = (2, 4, 6, 8)
    hall_spots = (0, 1, 3, 5, 7, 9, 10)
    destination = {"A": 0, "B": 1, "C": 2, "D": 3}
    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

    room_size = len(lines[0])

    hallway_start = tuple(None for _ in range(len(room_map) + len(hall_spots)))

    @lru_cache(maxsize=None)
    def helper(hallway, rooms):
        if rooms == (("A",) * room_size, ("B",) * room_size, ("C",) * room_size, ("D",) * room_size):
            return 0

        best_cost = float('inf')
        for i, square in enumerate(hallway):  # Move from the hallway into a room.
            if square is None:
                continue
            dest = destination[square]
            can_move = True
            for roommate in rooms[dest]:
                if roommate is not None and roommate != square:
                    # Foreigner in room: can't move there.
                    can_move = False
                    break
            if not can_move:
                continue
            offset = 1 if room_map[dest] > i else -1
            for j in range(i + offset, room_map[dest] + offset, offset):
                if hallway[j] is not None:
                    can_move = False
                    break
            if not can_move:
                continue
            none_count = sum(elem is None for elem in rooms[dest])
            new_room = (None,) * (none_count - 1) + (square,) * (room_size - none_count + 1)
            steps = none_count + abs(i - room_map[dest])
            cost = steps * costs[square]
            helper_result = helper(hallway[:i] + (None,) + hallway[i + 1:], rooms[:dest] + (new_room,)
                                   + rooms[dest + 1:])
            new_cost = cost + helper_result
            if new_cost < best_cost:
                best_cost = new_cost
        for i, room in enumerate(rooms):  # Move from a room into the hallway.
            wants_to_move = False
            for elem in room:
                if elem is not None and destination[elem] != i:
                    wants_to_move = True
            if not wants_to_move:
                continue
            none_count = sum(elem is None for elem in room)
            steps = none_count + 1
            square = room[none_count]
            for hall_destination in hall_spots:
                destination_steps = steps + abs(hall_destination - room_map[i])
                destination_cost = destination_steps * costs[square]
                blocked = False
                for j in range(min(hall_destination, room_map[i]), max(hall_destination, room_map[i])+1):
                    if hallway[j] is not None:
                        blocked = True
                        break
                if blocked:
                    continue
                new_room = (None,) * (none_count + 1) + room[none_count + 1:]
                helper_result = helper(
                    hallway[:hall_destination] + (square,) + hallway[hall_destination + 1:],
                    rooms[:i] + (new_room,) + rooms[i + 1:])
                new_cost = destination_cost + helper_result
                if new_cost < best_cost:
                    best_cost = new_cost

        return best_cost

    cost = helper(hallway_start, lines)
    return cost


if __name__ == "__main__":
    main()
