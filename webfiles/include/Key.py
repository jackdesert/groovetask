#!/usr/bin/env python
import unittest
class Key:
    # Constructor args:
    # either in_pri is blank and in_cat is a string such as '002_005'
    # meaning category is 2 and priority is 5, or...
    # in_cat is an integer representing  category, and in_pri is an integer
    # representing priority
    # Examples:
    # key = Key.Key(in_cat, in_pri)
    # Alternatively, you can call it with just one argument
    # key = Key.Key(in_cat)
    # Which means in_cat really represents the whole cat_pri_string
    def __init__(self, in_cat, in_pri = None):
        # print("lenth of input is", len(input))
        # define 'private' variables


        # Assign values to 'private' variables
        if (in_pri == None):
            if(len(in_cat) == 7):
                self.__cat = int(in_cat[0:3])
                self.__pri = int(in_cat[4:7])
            else:
                raise ValueError('Wrong input length in Key()')
        else:
            self.__cat = int(in_cat)
            self.__pri = int(in_pri)
    def get_cat(self):
        return(self.__cat)
    def get_pri(self):
        return(self.__pri)
    def get_str(self):
        answer = m3(self.__cat) + '_' + m3(self.__pri)
        return(answer)


# m3() is an auxilary function (non-class) that accepts strings or ints
# Makes it a three-digit string with leading zeros
def m3(input):
    input = str(input)  # Convert to a string if not already
    if (len(input) == 3):
        output = input
    elif (len(input) == 2):
        output = '0' + input
    elif (len(input) == 1):
        output = '00' + input
    else:
        raise ValueError("m3 was given a None input")
    return(output)

class MenuTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_key_exists(self):
        a_key = Key(5,6)
        self.assertEquals(a_key.get_cat(), 5)
        self.assertEquals(a_key.get_pri(), 6)
        a_key = Key('002_351')
        self.assertEquals(a_key.get_cat(), 2)
        self.assertEquals(a_key.get_pri(), 351)
        self.assertEquals(a_key.get_str(), '002_351')
    def test_creation(self):
        # Should fail from incorrect length
        self.assertRaises(ValueError, Key,'001002')
        # Should fail during 'int' conversion of 'f'
        self.assertRaises(ValueError, Key, 5, 'f')





if __name__ == '__main__':
    unittest.main()
