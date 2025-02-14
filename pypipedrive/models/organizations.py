from pypipedrive.orm.model import Model
from pypipedrive.orm import fields as F


class Organizations(Model):

    id          = F.IntegerField("id", readonly=True)
    name        = F.TextField("name")
    add_time    = F.DatetimeField("add_time", readonly=True) # "2025-02-10T18:06:06Z"
    update_time = F.DatetimeField("update_time", readonly=True) # "2025-02-13T13:20:25Z"
    visible_to  = F.IntegerField("visible_to")
    owner_id    = F.IntegerField("owner_id")
    label_ids   = F.LabelIdsField("label_ids")
    is_deleted  = F.BooleanField("is_deleted", readonly=True)
    address     = F.AddressField("address")

    # Custom field names
    custom_etp_reel          = F.IntegerField("938cf6e69616565e93c1de7d2d2008b31b627624")
    custom_etp_potentiel     = F.IntegerField("182fe8edbf9b2d2ae986220df40daf181c2dd067")
    custom_etp_potentiel_max = F.IntegerField("be4510e35fd2f092d73652d28d0f6409cf45ead3")

    # Custom fields monétaire with units
    # E_D: Heure d'insertion 2/3 (custom currency)
    # EUR: Euros (Eu) (native field)
    # A_3: CA Mensuel (CA) (custom currency)
    # 5_7: Équivalent Temps Plein (custom currency)
    custom_marge_h_reel        = F.MonetaryField("47f8b4345e991e0206b4606588024ab0e0e61ecb")
    custom_marge_h_potentielle = F.MonetaryField("e25054e292950580cdb39275193a44d6c2267a00")
    custom_marge_h_moyenne     = F.MonetaryField("9678f9efd5cb1b3d9c031b9b97714438fbb10633")
    custom_siren               = F.TextField("73098432f490213cb3277506bf6bec4b386cc79a")
    custom_siret               = F.TextField("dd04def2fb6fa5afeb883b60a8c23071dc265374")

    class Meta:
        id_name       = "id"
        entity_name   = "organizations"