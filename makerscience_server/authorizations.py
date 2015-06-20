from dataserver.authorization import GuardianAuthorization

class MakerScienceAPIAuthorization(GuardianAuthorization):

    def read_detail(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone authenticated or not read detail
        """
        self.generic_base_check(object_list, bundle)
        return True

    def read_list(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone authenticated or not read list
        """
        self.generic_base_check(object_list, bundle)
        return object_list

    def create_detail(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone with add permissions
        *FIXME* : this override should not be required since we assign global edit
        rights to all new users (see .models.py)

        """
        self.generic_base_check(object_list, bundle)
        return bundle.request.user.has_perm(self.create_permission_code)
