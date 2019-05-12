
class GManager:

    def map_headers(self, headers, minerals):
        data_map = {}
        print("You have entered the following headers for your block model:")
        for index in range(len(headers)):
            print("\t{}. {}".format(index + 1, headers[index]))
        print("Please tell me, which one of those hearders refers to:")
        relevant_headers = ['x', 'y', 'z', 'weight']
        for header in relevant_headers:
            print("{}: ".format(header), end = '')
            response = self.get_valid_index(headers) - 1
            data_map[header] = headers[response]
        data_map["grade"] = {}
        for mineral in minerals:
            print("{} grade: ".format(mineral), end = '')
            response = self.get_valid_index(headers) - 1
            data_map["grade"][mineral] = headers[response]
        return data_map

    def get_valid_index(self, data):
        response = -1
        while response > len(data) or response <= 0:
            try:
                response = int(input())
            except:
                f = input("exit? y/n\n")
                if f == 'y':
                    exit()
                continue
        return response


    def grade_to_percentage(self, value, weight, unit):
        if unit == 'tonn':
            return value / weight
        elif unit == 'oz/tonn':
            return value * 32000 / weight
        elif unit == 'ppm':
            return value / 10000
        else:
            return value