

class Calc_average():
    def __init__(self):
        pass


    def run(self, avg_list):
        """
            avg_list: list of ints
        
        """
        number_of_items = 0
        sum_of_items = 0

        for item in avg_list:
            if not isinstance(item, int) or not isinstance(item, float):
                return "Item ist kein Integer!"
            else:
                number_of_items += 1
                sum_of_items += item

        return sum_of_items / number_of_items