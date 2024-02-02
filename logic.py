def validate_positions(requested_positions, stack, PLAY_AREA_HEIGHT, PLAY_AREA_WIDTH):
	for candidate_y, candidate_x in requested_positions:
		if candidate_y <= 0 or candidate_y > PLAY_AREA_HEIGHT:
			return False

		if candidate_x < 0 or candidate_x >= PLAY_AREA_WIDTH:
			return False

		if (candidate_y, candidate_x) in stack['positions']:
			return False

	return True

def is_inside_stack(requested_positions, stack, PLAY_AREA_HEIGHT):
	for candidate_point in requested_positions:
		if candidate_point in stack['positions']:
			return True

		candidate_y, _ = candidate_point

		if candidate_y > PLAY_AREA_HEIGHT:
			# last row
			return True

	return False

def increase_stack(piece, stack, COLOR_MAP):
	affected_lines = set()
	color = COLOR_MAP[piece]

	for position in piece.current_positions:
		stack['positions'][position] = color
		line, _ = position
		affected_lines.add(line)

	return affected_lines

def check_cleared_lines(stack, affected_lines, PLAY_AREA_WIDTH):
	cleared_lines = list()

	for line in affected_lines:
		line_cleared = True
		for x in range(PLAY_AREA_WIDTH):
			if (line, x) not in stack['positions']:
				line_cleared = False
				break

		if line_cleared:
			cleared_lines.append(line)

	return cleared_lines

def clear_lines(lines, stack):
	def count_lines_above(line):
		cnt = 0

		for cleared_line in lines:
			if line < cleared_line:
				cnt += 1

		return cnt

	new_positions = dict()

	max_line = max(lines)
	# update remaining stack positions
	for position, color in stack['positions'].items():
		y, x = position

		if y in lines:
			continue

		if y > max_line:
			# current position is below cleared lines
			# position doesn't need to be updated
			new_positions[position] = color
		else:
			new_position = (y + count_lines_above(y), x)
			new_positions[new_position] = color

	stack['previous_positions'] = stack['positions']
	stack['positions'] = new_positions
	