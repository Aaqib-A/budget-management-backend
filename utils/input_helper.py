from  user.models import User
# from category.models import Category

from utils.constants import ROLES

class RequestInputHelper():
    def __init__(self, data:dict, user:User=None):
        self.data = data.copy()
        self.user = user

    """     
    def __replace_string_to_array(self, param):

        if param in self.data:
            
            # elif type(self.data[param]) != list:
            if not isinstance(self.data[param], list):

                data_list = self.data.getlist(param)
                # self.data.setlist(param, data_list)

                if data_list and  "," in data_list[0]:
                    data_list = data_list[0]
                    data_list = data_list.replace("'", "")
                    data_list = data_list.replace("\"", "")
                    data_list = data_list.replace("[", "")
                    data_list = data_list.replace("]", "")
                    data_list = data_list.split(",")

                    data_list = [str(each_data).strip() for each_data in data_list]
                    self.data[param] = data_list

    def __replace_array_to_str(self, param):
        list_to_str = ','.join([str(elem) for elem in self.data[param]])
        self.data[param] = list_to_str

    def content_categories_helper(self):
        param = "categories"
        self.__replace_string_to_array(param)
        self.__replace_array_to_str(param) 
    """
        

    def category_post_user(self):
        """
        Automatically assign user to api caller if the role is Customer
        """

        if self.user.role == ROLES.CUSTOMER.value:
            self.data["user"] = self.user.user_id

    
    def category_patch_user(self):
        """
        Author role should not update user field 
        """

        if self.user.role == ROLES.CUSTOMER.value:
            if "user" in self.data.keys():
                self.data.pop("user")

    def created_modified_by_patch(self):
        """
        Update modified_by to self user at the time of patch api. Also, removes key created_by if it is present
        """

        self.data['modified_by'] = self.user.user_id
        if "created_by" in self.data.keys():
            self.data.pop("created_by")

    def created_modified_by_post(self):
        """
        Update created_by to self user at the time of post api. Also, removes key modified_by if it is present
        """
        
        self.data["created_by"] = self.user.user_id
        if "modified_by" in self.data.keys():
            self.data.pop("modified_by")

    def return_data(self):
        return self.data