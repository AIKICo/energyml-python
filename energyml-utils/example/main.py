# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import json
import re
from dataclasses import fields

from energyml.eml.v2_3.commonv2 import *
from energyml.eml.v2_3.commonv2 import AbstractObject
from energyml.resqml.v2_0_1.resqmlv2 import DoubleHdf5Array
from energyml.resqml.v2_0_1.resqmlv2 import TriangulatedSetRepresentation as Tr20
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    FaultInterpretation,
    ContactElement,
    AbstractPoint3DArray,
    AbstractColorMap,
)

# from src.energyml.utils.data.hdf import *
from src.energyml.utils.data.helper import get_projected_uom, is_z_reversed
from src.energyml.utils.epc import *
from src.energyml.utils.introspection import *
from src.energyml.utils.manager import *
from src.energyml.utils.serialization import *
from src.energyml.utils.validation import (
    patterns_validation,
    dor_validation,
    validate_epc,
    correct_dor,
)
from src.energyml.utils.xml import *
from src.energyml.utils.data.datasets_io import HDF5FileReader, get_path_in_external_with_path

fi_cit = Citation(
    title="An interpretation",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

fi = FaultInterpretation(
    citation=fi_cit,
    uuid=gen_uuid(),
    object_version="0",
)

tr_cit = Citation(
    title="--",
    # title="test title",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

dor = DataObjectReference(
    uuid=fi.uuid,
    title="a DOR title",
    object_version="0",
    qualified_type="a wrong qualified type",
)

dor_correct = DataObjectReference(
    uuid=fi.uuid,
    title="a DOR title",
    object_version="0",
    qualified_type="resqml23.TriangulatedSetRepresentation",
)

tr = TriangulatedSetRepresentation(
    citation=tr_cit,
    uuid=gen_uuid(),
    represented_object=dor,
)


def tests_0():
    print(list_energyml_modules())
    print(dict_energyml_modules())
    # print(get_all_energyml_classes())

    print(fields(Activity)[0].metadata)

    print(epoch_to_date(epoch()))
    print(date_to_epoch("2024-03-05T17:50:17.757+01:00"))
    print(epoch_to_date(date_to_epoch("2024-03-05T17:50:17.757+01:00")))

    print(serialize_xml(tr_cit))

    print(serialize_json(tr, JSON_VERSION.XSDATA))
    print(tr.citation)
    print(get_obj_uuid(tr))
    print("path: ", gen_energyml_object_path(tr))

    print(dir(Citation))
    print(get_class_attributes(Citation))

    alist = ["a", "b", "c", "d"]
    adict = {"a": 10}

    print("==>", get_object_attribute(alist, "0"))
    print("==>", get_object_attribute(adict, "a"))
    print("==>", get_object_attribute(tr, "citation.title"))

    print(re.split(r"(?<!\\)\.+", r"[Cc]itation.[Tt]it\.*"))
    print("==>", get_object_attribute_rgx(fi, r"[Cc]itation.[Tt]it\.*"))

    # print("==>", type(cit), type(Citation))
    # print("==>", type(cit) == type, type(Citation) == type)
    # print("==>", isinstance(cit, type), isinstance(Citation, type))

    print(gen_uuid())
    print(re.match(r"Obj[A-Z].*", "ObjTriangulatedSetRepresentation"))
    print(re.match(r"Obj[A-Z].*", "TriangulatedSetRepresentation"))


def file_test():
    print(get_class_pkg_version(TriangulatedSetRepresentation))
    print(get_content_type_from_class(TriangulatedSetRepresentation))

    path = "D:/Geosiris/Github/energyml/#data/TriangulatedSetRepresentation_2_2.xml"

    xml_content = ""
    with open(path, "r") as f:
        xml_content = f.read()

    print(get_xml_encoding(xml_content))
    print(get_root_type(get_tree(xml_content)))
    print(get_root_namespace(get_tree(xml_content)))
    print(find_schema_version_in_element(get_tree(xml_content)))
    print(get_class_name_from_xml(get_tree(xml_content)))

    print(get_class_from_name("energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation"))

    print(read_energyml_xml_str(xml_content))
    print(read_energyml_xml_file(path))


def tests_content_type():
    print(RGX_CONTENT_TYPE)

    print(parse_content_type("application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"))
    print(parse_content_type("application/vnd.openxmlformats-package.core-properties+xml").group("domain"))

    print(get_class_from_content_type("application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"))
    print(
        "CT 201 : ",
        get_class_from_content_type("application/x-resqml+xml;version=2.0;type=obj_HorizonInterpretation"),
    )
    print(parse_content_type("application/x-resqml+xml;version=2.0;type=obj_HorizonInterpretation"))

    print(get_class_from_content_type("application/vnd.openxmlformats-package.core-properties+xml"))

    print(get_content_type_from_class(tr))
    print(get_qualified_type_from_class(tr))
    print(
        get_qualified_type_from_class(DoubleHdf5Array()),
        get_class_from_qualified_type(get_qualified_type_from_class(DoubleHdf5Array())),
    )
    print(
        get_qualified_type_from_class(dor_correct),
        get_class_from_qualified_type(get_qualified_type_from_class(dor_correct)),
    )

    print(gen_energyml_object_path(tr, EpcExportVersion.EXPANDED))
    print(gen_energyml_object_path(tr))


def tests_epc():
    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )
    print(serialize_json(epc.gen_opc_content_type(), JSON_VERSION.XSDATA))
    print(epc)
    epc.export_file("D:/Geosiris/Github/energyml/energyml-python/test.epc")
    epc.export_version = EpcExportVersion.EXPANDED
    epc.export_file("D:/Geosiris/Github/energyml/energyml-python/test_EXPANDED.epc")
    epc.core_props = None
    epc.export_file("D:/Geosiris/Github/energyml/energyml-python/test_no_core.epc")

    epc201 = Epc.read_file("D:/Geosiris/OSDU/manifestTranslation/#Data/VOLVE_STRUCT.epc")
    print(epc201)

    print(f"NB errors {len(validate_epc(epc201))}")

    correct_dor(epc201.energyml_objects)

    err_after_correction = validate_epc(epc201)
    print(f"NB errors after correction {len(err_after_correction)}")

    for err in err_after_correction:
        print(err)


def tests_dor():
    import json

    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )

    print(EPCRelsRelationshipType.DESTINATION_OBJECT.get_type())

    print(
        json.dumps(
            {k: [get_obj_uuid(x) for x in v] for k, v in get_reverse_dor_list(epc.energyml_objects).items()},
            indent=4,
        )
    )
    print(epc.compute_rels())


def test_verif():

    print(get_class_fields(tr))
    for err in patterns_validation(tr):
        print(err)

    print("DOR verif no fi")
    for err in dor_validation([tr]):
        print(err)

    print("DOR verif with fi")
    for err in dor_validation([tr, fi]):
        print(err)


def test_ast():
    import ast

    exp = ast.parse("Optional[Union[ExistenceKind, str]]", mode="eval")
    print(exp.body.__dict__)
    print(exp.body.value.__dict__)
    print(exp.body.slice.__dict__)
    print(tr.__class__.__dataclass_fields__["aliases"])
    print(tr.__class__.__dataclass_fields__["aliases"].default_factory())
    print(tr.__class__.__module__)
    print(get_class_pkg(tr))

    print(tr.__class__.__dict__)

    print(get_class_fields(tr))
    print(ast.parse("TriangulatedSetRepresentation"))
    print(eval("TriangulatedSetRepresentation"))
    print(eval("Optional[Union[ExistenceKind, str]]"))
    print(list(eval("Optional[Union[ExistenceKind, str]]").__args__))
    ll = list(eval("Optional[Union[ExistenceKind, str]]").__args__)
    ll.remove(type(None))
    if type(None) in ll:
        ll.remove(type(None))
    print(ll)
    print(list(eval("List[ObjectAlias]").__args__))
    print(random_value_from_class(tr.__class__))


def test_introspection():
    print(search_attribute_matching_type(tr, "int"))
    print(search_attribute_matching_type(tr, "float"))
    print(search_attribute_matching_type(tr, "list"))
    print(search_attribute_matching_type(tr, "str"))
    print(search_attribute_matching_type(tr, "^str$"))
    print(search_attribute_matching_type(tr, "Citation"))
    print(search_attribute_matching_type(tr, "DataObjectreference"))
    print(search_attribute_matching_type_with_path(tr, "DataObjectreference"))
    print(class_match_rgx(ContactElement, "DataObjectreference", super_class_search=False))
    print(class_match_rgx(ContactElement, "DataObjectreference", super_class_search=True))
    print(Enum in ExistenceKind.__bases__)
    print(Enum in TriangulatedSetRepresentation.__bases__)
    print(is_primitive(int))
    print(is_primitive(str))
    print(is_primitive(TriangulatedSetRepresentation))
    print(is_primitive(Citation))
    print(is_primitive(ExistenceKind))
    print(ExistenceKind.__bases__)
    print(Enum in ExistenceKind.__bases__)
    print(get_class_fields(tr))
    print(list(get_class_attributes(tr)))
    print(get_class_fields(tr)["citation"])

    print(EPCRelsRelationshipType._member_names_)
    print(EPCRelsRelationshipType["DESTINATION_OBJECT"].value)
    print(random_value_from_class(EPCRelsRelationshipType))
    print(random_value_from_class(EPCRelsRelationshipType))
    print(TriangulatedSetRepresentation.__dataclass_params__)

    # print(random_value_from_class(int))
    print(serialize_xml(random_value_from_class(TriangulatedSetRepresentation)))
    # print(serialize_json(random_value_from_class(TriangulatedSetRepresentation)))

    print(search_attribute_matching_name_with_path(tr, "[tT]it.*"))
    print(search_attribute_matching_name(tr, "[tT]it.*"))

    print(AbstractPoint3DArray.__dict__)
    print(TriangulatedSetRepresentation.__dict__)
    print(get_sub_classes(AbstractObject))
    print(list(filter(lambda _c: not is_abstract(_c), get_sub_classes(AbstractObject))))
    print(AbstractColorMap.__name__.startswith("Abstract"))
    print(is_abstract(AbstractColorMap))

    # print(object.__dict__)
    # print(hasattr(object, "__dataclass_fields__"))
    # print(get_class_methods(TriangulatedSetRepresentation))
    # print(get_class_methods(object))
    # print(len(object.__class__))
    # print(type(TriangulatedSetRepresentation.Meta), isinstance(TriangulatedSetRepresentation.Meta, type))
    # print(type(HDF5FileReader.read_array), isinstance(HDF5FileReader.read_array, type))

    print(get_class_methods(object))
    print(get_class_methods(HDF5FileReader))
    print(get_class_methods(TriangulatedSetRepresentation))

    print(f"object: {is_abstract(object)}")
    print(f"HDF5FileReader: {is_abstract(HDF5FileReader)}")
    print(f"TriangulatedSetRepresentation: {is_abstract(TriangulatedSetRepresentation)}")

    # print("HDF5FileReader")
    # for func in dir(HDF5FileReader):
    #     if callable(getattr(HDF5FileReader, func)) and not func.startswith("__"):
    #         print(f"\t{func} {type(getattr(HDF5FileReader, func))}")
    print(get_classes_matching_name(TriangulatedSetRepresentation, "Abstract.*"))
    # print(get_matching_class_attribute_name(ExternalDataArrayPart, "(PathInHdfFile|PathInExternalFile)"))
    # print(object.__module__)
    # print(serialize_xml(random_value_from_class(PointSetRepresentation)))
    # print(search_attribute_matching_type(random_value_from_class(PointSetRepresentation), "AbstractGeometry"))
    print(get_sub_classes(AbstractPoint3DArray))

    # =====================================================================

    poly = read_energyml_xml_file("../rc/polyline_set_for_array_tests.xml")

    # print(serialize_xml(poly))

    print("=====] ", r"ClosedPolylines.\d+")
    for array_path, array_value in search_attribute_matching_name_with_path(poly, r"ClosedPolylines.\d+"):
        print(f"{array_path}\n\t{array_value}")

    print("=====] ", r"ClosedPolylines.values.\d+")
    for array_path, array_value in search_attribute_matching_name_with_path(poly, r"ClosedPolylines.values.\d+"):
        print(f"{array_path}\n\t{array_value}")

    print("=====] ", r"LinePatch.\d+")
    for array_path, array_value in search_attribute_matching_name_with_path(poly, r"LinePatch.\d+"):
        print(f"{array_path}\n\t{array_value}")


def tests_hdf():
    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )

    tr_list = list(
        filter(
            lambda e: e.__class__.__name__ == "TriangulatedSetRepresentation",
            epc.energyml_objects,
        )
    )
    print(len(epc.energyml_objects))
    # print(tr_list)

    for o in tr_list:
        print(o.__class__)
        print(get_path_in_external_with_path(o))
        exit(0)


def test_local_depth_crs():
    # Fails because the xsi:type="VerticalCrsEpsgCode" doesn't
    # contain the namespace : xsi:type="eml:VerticalCrsEpsgCode"
    try:
        depth3d = read_energyml_xml_file("../rc/obj_LocalDepth3dCrs_716f6472-18a3-4f19-a57c-d4f5642ccc53.xml")
        print(serialize_json(depth3d, JSON_VERSION.XSDATA))
        print(serialize_xml(depth3d))
    except Exception as e:
        print(e)


def test_crs():
    from energyml.eml.v2_3.commonv2 import LocalEngineeringCompoundCrs

    crs = random_value_from_class(LocalEngineeringCompoundCrs)
    print(is_z_reversed(crs))


def test_get_projected_uom():
    # Fails because the xsi:type="VerticalCrsEpsgCode" doesn't
    # contain the namespace : xsi:type="eml:VerticalCrsEpsgCode"
    try:
        depth3d = read_energyml_xml_file("../rc/obj_LocalDepth3dCrs_716f6472-18a3-4f19-a57c-d4f5642ccc53.xml")
        print(get_projected_uom(depth3d).value)
    except Exception as e:
        print(e)


def test_wellbore_marker_frame_representation():
    # Fails because the xsi:type="VerticalCrsEpsgCode" doesn't
    # contain the namespace : xsi:type="eml:VerticalCrsEpsgCode"
    try:
        depth3d = read_energyml_xml_file(
            "../rc/obj_WellboreMarkerFrameRepresentation_2f8778ca-6a09-446b-b25d-b725ec759a70.xml"
        )
        print("read_success")
        # print(serialize_json(depth3d, JSON_VERSION.XSDATA))
        print(serialize_json(depth3d, JSON_VERSION.OSDU_OFFICIAL))
        # print(serialize_xml(depth3d))
    except Exception as e:
        print(e)
        raise e
        # print(traceback.print_stack())


def test_obj_attribs():
    print(get_obj_pkg_pkgv_type_uuid_version(dor_correct))
    print(get_obj_pkg_pkgv_type_uuid_version(tr))

    print(get_obj_uri(dor_correct, "coucou"))
    print(get_obj_uri(tr, "coucou"))


def test_copy_values():
    data_in = {
        "a": {"b": "v_0", "c": "v_1"},
        "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
        "objectVersion": "Resqml 2.0",
        "non_existing": 42,
    }
    data_out = {
        "a": None,
        "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
        "object_version": "Resqml 2.0",
    }
    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=True,
        ignore_case=True,
    )


def class_field():
    print(get_class_fields(tr)["citation"])
    print(get_class_pkg_version(tr))
    print(create_energyml_object("resqml22.TriangulatedSetRepresentation"))
    ext_20 = create_energyml_object("application/x-eml+xml;version=2.0;type=obj_EpcExternalPartReference")
    print(ext_20)
    print(gen_energyml_object_path(ext_20))
    print(create_external_part_reference("2.0", "my_h5"))

    print(parse_content_or_qualified_type("application/x-eml+xml;version=2.0;type=obj_EpcExternalPartReference"))
    print(
        get_domain_version_from_content_or_qualified_type(
            "application/x-eml+xml;version=2.0;type=obj_EpcExternalPartReference"
        )
    )
    print(get_domain_version_from_content_or_qualified_type("resqml20.obj_EpcExternalPartReference"))

    # print(create_external_part_reference("2.2", "myfile.h5"))
    # print(create_external_part_reference("2.0", "myfile.h5"))


def test_dor_conversion():

    print(serialize_json(dor_correct))
    print(serialize_json(as_dor(dor_correct, "eml20.DataObjectReference")))


if __name__ == "__main__":
    # tests_0()
    # tests_content_type()
    #
    # tests_epc()
    # tests_dor()
    # test_verif()
    # test_ast()
    # test_introspection()
    #
    # tests_hdf()
    # test_local_depth_crs()
    # test_wellbore_marker_frame_representation()
    #
    # test_obj_attribs()
    # test_copy_values()
    # class_field()
    # test_get_projected_uom()
    # test_crs()
    # test_dor_conversion()
    print(get_obj_uri(tr, "coucou"))

    tr201 = Tr20(
        citation=tr_cit,
        uuid=gen_uuid(),
    )
    print(get_obj_uri(tr201, "coucou"))
