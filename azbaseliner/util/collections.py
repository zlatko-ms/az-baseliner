class ListUtils(object):
    @classmethod
    def splitIntoChunks(ctx, items: list, chunkSize: int) -> list:
        """splits list into sublist of max chunkSize"""
        x = [items[i : i + chunkSize] for i in range(0, len(items), chunkSize)]
        return x


class DictUtils(object):
    @classmethod
    def mergeDicts(ctx, dict_1: dict, dict_2: dict) -> dict:
        """merges two dicts with addition of elements in an array for same key"""
        dict_3 = {**dict_1, **dict_2}
        for key, value in dict_3.items():
            if key in dict_1 and key in dict_2:
                theValue1 = dict_1[key]
                theValue2 = dict_2[key]
                if (type(theValue1) == list) and (type(theValue2) == list):
                    dict_3[key] = [*theValue1, *theValue2]
                elif (type(theValue1) == dict) and (type(theValue2) == dict):
                    dict_3[key] = ctx.mergeDicts(theValue1, theValue2)
                else:
                    dict_3[key] = [value, dict_1[key]]
        return dict_3
