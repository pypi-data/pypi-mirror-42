import logging
from hashlib import sha256

import six
from django.contrib.auth import get_user_model
# from six.moves.urllib.parse import quote
# from six.moves.urllib.parse import unquote
from saml2 import SAMLError
from saml2.ident import code, decode
from saml2.s_utils import rndbytes
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS
from saml2.saml import NAMEID_FORMAT_PERSISTENT
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_UNSPECIFIED
from saml2.saml import NameID

from django_saml2_framework.utils import get_cache_store

logger = logging.getLogger('django')


class UserIdentity(object):
    @property
    def default_attributes(self):
        return {
            self.User.USERNAME_FIELD: self.User.USERNAME_FIELD,
            self.User.EMAIL_FIELD: self.User.EMAIL_FIELD,
            'first_name': 'first_name',
            'last_name': 'last_name',
        }

    @property
    def User(self):
        return get_user_model()

    def get_user(self, id):
        return self.User.objects.get(pk=id)

    def create_authn_identity(self, id, user=None):
        user = user or self.get_user(id)
        return self.user_to_ava(user, self.default_attributes)

    def user_to_ava(self, user, attributes):
        return {attr: getattr(user, obj_attr, None) for attr, obj_attr in attributes.items()}

    def ava_to_user(self, name_id, ava):
        pass


class ModelIdentDB(object):
    """ A class that handles identifiers of entities
     Keeps a list of all nameIDs returned per SP
    """

    def __init__(self, cache=None, cache_name=None, domain="", name_qualifier=""):
        # todo: do something with cache and cache_name
        self.cache = cache or get_cache_store()
        # if isinstance(db, six.string_types):
        #     self.db = shelve.open(db, protocol=2)
        # else:
        #     self.db = db
        self.prefix = 'ident'
        self.domain = domain
        self.name_qualifier = name_qualifier

    def _create_id(self, nformat, name_qualifier="", sp_name_qualifier=""):
        # raise Exception('_create_id')
        _id = sha256(rndbytes(32))
        if not isinstance(nformat, six.binary_type):
            nformat = nformat.encode('utf-8')
        _id.update(nformat)
        if name_qualifier:
            if not isinstance(name_qualifier, six.binary_type):
                name_qualifier = name_qualifier.encode('utf-8')
            _id.update(name_qualifier)
        if sp_name_qualifier:
            if not isinstance(sp_name_qualifier, six.binary_type):
                sp_name_qualifier = sp_name_qualifier.encode('utf-8')
            _id.update(sp_name_qualifier)
        return _id.hexdigest()

    def create_id(self, nformat, name_qualifier="", sp_name_qualifier=""):
        _id = self._create_id(nformat, name_qualifier, sp_name_qualifier)
        # todo: 
        # while _id in self.db:
        #     _id = self._create_id(nformat, name_qualifier, sp_name_qualifier)
        return _id

    def key(self, key):
        return '{}_{}'.format(self.prefix, key)

    def store(self, ident, name_id):
        """

        :param ident: user identifier
        :param name_id: NameID instance
        """
        # raise Exception('store')
        # One user may have more than one NameID defined
        name_ids = self.cache.get(self.key(ident), [])

        _cn = code(name_id)
        name_ids.append(_cn)
        self.cache.set(self.key(ident), name_ids)
        self.cache.set(self.key(_cn), ident)
        # self.db[name_id.text] = ident

    def remove_remote(self, name_id):
        """
        Remove a NameID to userID mapping

        :param name_id: NameID instance
        """
        raise Exception('remove_remote')
        # _cn = code(name_id)
        # _id = self.db[name_id.text]
        # try:
        #     vals = self.db[_id].split(" ")
        #     vals.remove(_cn)
        #     self.db[_id] = " ".join(vals)
        # except KeyError:
        #     pass

        # del self.db[name_id.text]

    def remove_local(self, sid):
        raise Exception('remove_local')
        # if isinstance(sid, unicode):
        #     sid = sid.encode("utf-8")

        # try:
        #     for val in self.db[sid].split(" "):
        #         try:
        #             nid = decode(val)
        #             del self.db[nid.text]
        #         except KeyError:
        #             pass
        #     del self.db[sid]
        # except KeyError:
        #     pass

    def get_nameid(self, userid, nformat, sp_name_qualifier, name_qualifier):
        _id = self.create_id(nformat, name_qualifier, sp_name_qualifier)

        # if nformat == NAMEID_FORMAT_EMAILADDRESS:
        #     if not self.domain:
        #         raise SAMLError("Can't issue email nameids, unknown domain")

        #     _id = "%s@%s" % (_id, self.domain)
        User = get_user_model()

        if nformat == NAMEID_FORMAT_EMAILADDRESS:
            _id = User._default_manager.filter(pk=userid).values(User.EMAIL_FIELD).first()[User.EMAIL_FIELD]
        elif nformat == NAMEID_FORMAT_UNSPECIFIED:
            _id = User._default_manager.filter(pk=userid).values(User.USERNAME_FIELD).first()[User.USERNAME_FIELD]
        elif nformat == NAMEID_FORMAT_PERSISTENT:
            # _id = userid
            # todo: pseudo random
            raise NotImplementedError(
                '{} does not implement the format for {}'.format(self.__name__, NAMEID_FORMAT_PERSISTENT))
        elif nformat == NAMEID_FORMAT_TRANSIENT:
            # _id = userid
            # todo: temporary thing
            raise NotImplementedError(
                '{} does not implement the format for {}'.format(self.__name__, NAMEID_FORMAT_TRANSIENT))

        nameid = NameID(format=nformat, sp_name_qualifier=sp_name_qualifier,
                        name_qualifier=name_qualifier, text=_id)

        self.store(userid, nameid)
        return nameid
        # raise Exception('get_nameid')

    def find_nameid(self, userid, **kwargs):
        """
        Find a set of NameID's that matches the search criteria.

        :param userid: User id
        :param kwargs: The search filter a set of attribute/value pairs
        :return: a list of NameID instances
        """
        res = []
        name_ids = self.cache.get(self.key(userid), [])

        for _cn in name_ids:
            name_id = decode(_cn)
            if kwargs:
                for key, _val in kwargs.items():
                    if getattr(name_id, key, None) != _val:
                        break
                else:
                    res.append(name_id)
            else:
                res.append(name_id)
        # raise Exception('find_nameid')
        logger.info('name_ids')
        logger.info([userid, name_ids])
        logger.info(res)
        return res

    def nim_args(self, local_policy=None, sp_name_qualifier="",
                 name_id_policy=None, name_qualifier=""):
        """

        :param local_policy:
        :param sp_name_qualifier:
        :param name_id_policy:
        :param name_qualifier:
        :return:
        """
        # raise Exception('nim_args')
        logger.info("local_policy: %s, name_id_policy: %s", local_policy, name_id_policy)

        if name_id_policy and name_id_policy.sp_name_qualifier:
            sp_name_qualifier = name_id_policy.sp_name_qualifier
        # else:
        #     sp_name_qualifier = sp_name_qualifier

        if name_id_policy and name_id_policy.format:
            nameid_format = name_id_policy.format
        elif local_policy:
            nameid_format = local_policy.get_nameid_format(sp_name_qualifier)
        else:
            raise SAMLError("Unknown NameID format")

        if not name_qualifier:
            name_qualifier = self.name_qualifier

        return {"nformat": nameid_format,
                "sp_name_qualifier": sp_name_qualifier,
                "name_qualifier": name_qualifier}

    def construct_nameid(self, userid, local_policy=None,
                         sp_name_qualifier=None, name_id_policy=None,
                         name_qualifier=""):
        """ Returns a name_id for the object. How the name_id is
        constructed depends on the context.

        :param local_policy: The policy the server is configured to follow
        :param userid: The local permanent identifier of the object
        :param sp_name_qualifier: The 'user'/-s of the name_id
        :param name_id_policy: The policy the server on the other side wants
            us to follow.
        :param name_qualifier: A domain qualifier
        :return: NameID instance precursor
        """
        args = self.nim_args(local_policy, sp_name_qualifier, name_id_policy)

        if name_qualifier:
            args["name_qualifier"] = name_qualifier
        else:
            args["name_qualifier"] = self.name_qualifier
        # raise Exception('WTF NAMEID')
        return self.get_nameid(userid, **args)

    def transient_nameid(self, userid, sp_name_qualifier="", name_qualifier=""):
        raise Exception('transient_nameid')
        # return self.get_nameid(userid, NAMEID_FORMAT_TRANSIENT, sp_name_qualifier, name_qualifier)

    def persistent_nameid(self, userid, sp_name_qualifier="", name_qualifier=""):
        raise Exception('persistent_nameid')
        # nameid = self.match_local_id(userid, sp_name_qualifier, name_qualifier)
        # if nameid:
        #     return nameid
        # else:
        #     return self.get_nameid(userid, NAMEID_FORMAT_PERSISTENT, sp_name_qualifier, name_qualifier)

    def find_local_id(self, name_id):
        """
        Only find persistent IDs

        :param name_id:
        :return:
        """
        raise Exception('find_local_id')
        # try:
        #     return self.db[name_id.text]
        # except KeyError:
        #     logger.debug("name: %s", name_id.text)
        #     #logger.debug("id sub keys: %s", self.subkeys())
        #     return None

    def match_local_id(self, userid, sp_name_qualifier, name_qualifier):
        raise Exception('match_local_id')
        # try:
        #     for val in self.db[userid].split(" "):
        #         nid = decode(val)
        #         if nid.format == NAMEID_FORMAT_TRANSIENT:
        #             continue
        #         snq = getattr(nid, "sp_name_qualifier", "")
        #         if snq and snq == sp_name_qualifier:
        #             nq = getattr(nid, "name_qualifier", None)
        #             if nq and nq == name_qualifier:
        #                 return nid
        #             elif not nq and not name_qualifier:
        #                 return nid
        #         elif not snq and not sp_name_qualifier:
        #             nq = getattr(nid, "name_qualifier", None)
        #             if nq and nq == name_qualifier:
        #                 return nid
        #             elif not nq and not name_qualifier:
        #                 return nid
        # except KeyError:
        #     pass

        # return None

    def handle_name_id_mapping_request(self, name_id, name_id_policy):
        """

        :param name_id: The NameID that specifies the principal
        :param name_id_policy: The NameIDPolicy of the requester
        :return: If an old name_id exists that match the name-id policy
            that is return otherwise if a new one can be created it
            will be and returned. If no old matching exists and a new
            is not allowed to be created None is returned.
        """
        raise Exception('handle_name_id_mapping_request')
        # _id = self.find_local_id(name_id)
        # if not _id:
        #     raise Unknown("Unknown entity")

        # # return an old one if present
        # for val in self.db[_id].split(" "):
        #     _nid = decode(val)
        #     if _nid.format == name_id_policy.format:
        #         if _nid.sp_name_qualifier == name_id_policy.sp_name_qualifier:
        #             return _nid

        # if name_id_policy.allow_create == "false":
        #     raise PolicyError("Not allowed to create new identifier")

        # # else create and return a new one
        # return self.construct_nameid(_id, name_id_policy=name_id_policy)

    def handle_manage_name_id_request(self, name_id, new_id=None,
                                      new_encrypted_id="", terminate=""):
        """
        Requests from the SP is about the SPProvidedID attribute.
        So this is about adding,replacing and removing said attribute.

        :param name_id: NameID instance
        :param new_id: NewID instance
        :param new_encrypted_id: NewEncryptedID instance
        :param terminate: Terminate instance
        :return: The modified name_id
        """
        raise Exception('handle_manage_name_id_request')
        # _id = self.find_local_id(name_id)

        # orig_name_id = copy.copy(name_id)

        # if new_id:
        #     name_id.sp_provided_id = new_id.text
        # elif new_encrypted_id:
        #     # TODO
        #     pass
        # elif terminate:
        #     name_id.sp_provided_id = None
        # else:
        #     #NOOP
        #     return name_id

        # self.remove_remote(orig_name_id)
        # self.store(_id, name_id)
        # return name_id

    def close(self):
        pass
        # if hasattr(self.db, 'close'):
        #     self.db.close()

    def sync(self):
        pass
        # if hasattr(self.db, 'sync'):
        #     self.db.sync()
