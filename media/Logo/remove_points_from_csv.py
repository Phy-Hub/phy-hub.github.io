def filter_dots_csv(input_path, output_path):
    # Dimensions based on your SVG coordinates
    svg_min_x = -4.0
    svg_width = 8.0

    # Calculate 1/64th margin on each side
    margin = 0.08  # 0.125

    # Define the "safe" zone boundaries
    left_boundary = svg_min_x + margin               # -3.875
    right_boundary = svg_min_x + svg_width - margin  # 3.875

    # Read the original comma-separated data
    with open(input_path, 'r') as file:
        data = file.read().strip()

    # Split by comma
    values = [v for v in data.split(',') if v.strip()]
    filtered_values = []

    # Process in pairs of 2 (x, y)
    for i in range(0, len(values), 2):
        x_str = values[i]
        y_str = values[i+1]

        try:
            x = float(x_str)

            # Only keep the (x, y) pair if x is strictly inside the boundaries
            if left_boundary <= x <= right_boundary:
                filtered_values.extend([x_str, y_str])

        except ValueError:
            continue # Skip if there's any weird non-number data

    # Write the filtered data back to a new CSV
    with open(output_path, 'w') as file:
        file.write(','.join(filtered_values))

    # Print a quick summary of what changed
    original_count = len(values) // 2
    filtered_count = len(filtered_values) // 2
    print(f"Original points: {original_count}")
    print(f"Filtered points: {filtered_count}")
    print(f"Successfully removed {original_count - filtered_count} points from the edges.")

# Run the function
filter_dots_csv('DS_Pattern.csv', 'DS_Pattern_filtered.csv')