import random

class GreedyAlgorithms:
    @staticmethod
    def get_algorithm(name, inputs, draw_func):
        algorithm_map = {
            "Fractional Knapsack": GreedyAlgorithms.fractional_knapsack,
            "Activity Selection": GreedyAlgorithms.activity_selection
        }
        return algorithm_map.get(name, lambda x, y: None)(inputs, draw_func)

    @staticmethod
    def fractional_knapsack(inputs, draw_func):
        capacity, items = inputs
        n = len(items)
        
        # Calculate value per weight ratio for each item
        for i in range(n):
            items[i]['ratio'] = items[i]['value'] / items[i]['weight']
        
        # Sort items by value/weight ratio in descending order
        items.sort(key=lambda x: x['ratio'], reverse=True)
        
        # Draw initial state
        draw_func({
            'type': 'knapsack',
            'items': items,
            'capacity': capacity,
            'current_weight': 0,
            'current_value': 0,
            'current_item': None,
            'selected_items': [],
            'step': 'Items sorted by value/weight ratio',
            'complete': False
        })
        yield

        current_weight = 0
        current_value = 0
        selected_items = []

        for i, item in enumerate(items):
            if current_weight + item['weight'] <= capacity:
                # Take whole item
                fraction = 1.0
                current_weight += item['weight']
                current_value += item['value']
                selected_items.append({**item, 'fraction': fraction})
                
                draw_func({
                    'type': 'knapsack',
                    'items': items,
                    'capacity': capacity,
                    'current_weight': current_weight,
                    'current_value': current_value,
                    'current_item': i,
                    'selected_items': selected_items,
                    'step': f"Added item {i+1} completely (Weight: {item['weight']}, Value: {item['value']})",
                    'complete': False
                })
                yield
                
            else:
                # Take fractional part
                remaining = capacity - current_weight
                if remaining > 0:
                    fraction = remaining / item['weight']
                    current_weight += remaining
                    current_value += item['value'] * fraction
                    selected_items.append({**item, 'fraction': fraction})
                    
                    draw_func({
                        'type': 'knapsack',
                        'items': items,
                        'capacity': capacity,
                        'current_weight': current_weight,
                        'current_value': current_value,
                        'current_item': i,
                        'selected_items': selected_items,
                        'step': f"Added {fraction:.2f} of item {i+1} (Weight: {remaining:.2f}, Value: {item['value'] * fraction:.2f})",
                        'complete': False
                    })
                    yield
                break

        # Show completion
        draw_func({
            'type': 'knapsack',
            'items': items,
            'capacity': capacity,
            'current_weight': current_weight,
            'current_value': current_value,
            'current_item': None,
            'selected_items': selected_items,
            'step': f'Knapsack filled! Total Value: {current_value:.2f}',
            'complete': True
        })
        yield True

    @staticmethod
    def activity_selection(inputs, draw_func):
        activities = inputs
        n = len(activities)
        
        # Sort activities by finish time
        activities.sort(key=lambda x: x['finish'])
        
        # Draw initial state
        draw_func({
            'type': 'activity',
            'activities': activities,
            'selected': [],
            'current': None,
            'last_selected': None,
            'step': 'Activities sorted by finish time',
            'complete': False
        })
        yield
        
        # Select first activity
        selected = [activities[0]]
        draw_func({
            'type': 'activity',
            'activities': activities,
            'selected': selected,
            'current': 0,
            'last_selected': 0,
            'step': f"Selected first activity: ({activities[0]['start']}-{activities[0]['finish']})",
            'complete': False
        })
        yield
        
        # Consider remaining activities
        last = 0
        for i in range(1, n):
            # If this activity has start time greater than or equal to the finish
            # time of previously selected activity, then select it
            if activities[i]['start'] >= activities[last]['finish']:
                selected.append(activities[i])
                draw_func({
                    'type': 'activity',
                    'activities': activities,
                    'selected': selected,
                    'current': i,
                    'last_selected': last,
                    'step': f"Selected activity {i+1}: ({activities[i]['start']}-{activities[i]['finish']})",
                    'complete': False
                })
                yield
                last = i
            else:
                draw_func({
                    'type': 'activity',
                    'activities': activities,
                    'selected': selected,
                    'current': i,
                    'last_selected': last,
                    'step': f"Skipped activity {i+1} (overlaps with activity {last+1})",
                    'complete': False
                })
                yield
        
        # Show completion
        draw_func({
            'type': 'activity',
            'activities': activities,
            'selected': selected,
            'current': None,
            'last_selected': last,
            'step': f'Completed! Selected {len(selected)} activities',
            'complete': True
        })
        yield True

    @staticmethod
    def generate_random_items(num_items=5):
        """Generate random items for knapsack"""
        import random
        items = []
        for i in range(num_items):
            items.append({
                'id': i + 1,
                'weight': random.randint(1, 20),
                'value': random.randint(10, 100)
            })
        return items

    @staticmethod
    def generate_random_activities(num_activities=6):
        """Generate random activities for activity selection"""
        import random
        activities = []
        current_time = 0
        
        for i in range(num_activities):
            duration = random.randint(1, 5)
            gap = random.randint(0, 3)
            start = current_time + gap
            finish = start + duration
            
            activities.append({
                'id': i + 1,
                'start': start,
                'finish': finish
            })
            current_time = finish
        
        # Shuffle activities
        random.shuffle(activities)
        return activities