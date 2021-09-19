import h5py
import time
from queue import Queue


def execute_extractor(filename):
    t0 = time.time()
    if not filename:
        return None
    metadata = extract_hdf_main(hdf_file_path=filename)
    print(metadata)
    t1 = time.time()
    metadata.update({"extract time": (t1 - t0)})
    return metadata


def extract_attribute_metadata(h5py_attributes):
    """Extracts metadata from h5py attribute manager classes.

    Parameters
    ----------
    h5py_attributes : h5py.AttributeManager
        h5py attribute manager class as returned by the .attrs method.

    Returns
    -------
    metadata_dictionary : dict
        Dictionary containing attribute data.

    """
    metadata_dictionary = {}

    for key, value in h5py_attributes.items():
        metadata_dictionary[key] = value

    return metadata_dictionary


def extract_group_metadata(h5py_group_obj):
    """Extracts metadata from h5py group objects.

    Parameters
    ----------
    h5py_group_obj : h5py.Group
        h5py group object.

    Returns
    -------

    """
    metadata_dictionary = dict()
    metadata_dictionary["name"] = h5py_group_obj.name
    metadata_dictionary["type"] = "group"
    metadata_dictionary["attributes"] = extract_attribute_metadata(h5py_group_obj.attrs)
    metadata_dictionary["keys"] = list(h5py_group_obj.keys())
    metadata_dictionary["parent"] = h5py_group_obj.parent.name

    return metadata_dictionary


def extract_dataset_metadata(h5py_dataset_obj):
    """Extracts metadata from h5py dataset objects.

    Parameters
    ----------
    h5py_dataset_obj : h5py.Dataset
        h5py dataset object.

    Returns
    -------

    """
    metadata_dictionary = dict()
    metadata_dictionary["name"] = h5py_dataset_obj.name
    metadata_dictionary["type"] = "dataset"
    metadata_dictionary["attributes"] = extract_attribute_metadata(h5py_dataset_obj.attrs)
    metadata_dictionary["parent"] = h5py_dataset_obj.parent.name
    metadata_dictionary["shape"] = h5py_dataset_obj.shape
    metadata_dictionary["dtype"] = h5py_dataset_obj.dtype.str
    metadata_dictionary["size"] = h5py_dataset_obj.size.item()
    metadata_dictionary["nbytes"] = h5py_dataset_obj.nbytes.item()
    metadata_dictionary["ndim"] = h5py_dataset_obj.ndim
    metadata_dictionary["compression"] = h5py_dataset_obj.compression

    return metadata_dictionary


def extract_file_metadata(h5py_file_obj):
    """Extracts metadata from h5py file objects.

    Parameters
    ----------
    h5py_file_obj : h5py.File
        h5py file object.

    Returns
    -------
    metadata_dictionary : dict
        Dictionary containing file object name and attributes.

    """
    metadata_dictionary = dict()
    metadata_dictionary["name"] = h5py_file_obj.name
    metadata_dictionary["type"] = "file"
    metadata_dictionary["attributes"] = extract_attribute_metadata(h5py_file_obj.attrs)

    return metadata_dictionary


def extract_hdf_main(hdf_file_path):
    """Extracts metadata from .hdf files.

    Parameters
    ----------
    hdf_file_path : str
        File path of .hdf file to process.

    Returns
    -------

    """
    t0 = time.time()
    metadata_dictionary = {"hdf": {}}

    try:
        hdf_file = h5py.File(hdf_file_path, "r")
    except:
        return metadata_dictionary

    file_obj_metadata = extract_file_metadata(hdf_file)
    metadata_dictionary["hdf"][hdf_file.name] = file_obj_metadata

    unprocessed = Queue()
    unprocessed.put(hdf_file)

    while not(unprocessed.empty()):
        current = unprocessed.get()

        if isinstance(current, h5py.Group):
            group_metadata_dictionary = extract_group_metadata(current)
            metadata_dictionary["hdf"][current.name] = group_metadata_dictionary
            for value in current.values():
                unprocessed.put(value)
        elif isinstance(current, h5py.Dataset):
            dataset_metadata_dictionary = extract_dataset_metadata(current)
            metadata_dictionary["hdf"][current.name] = dataset_metadata_dictionary
        elif isinstance(current, h5py.File):
            for value in current.values():
                unprocessed.put(value)

    metadata_dictionary.update({"extract time": time.time() - t0})

    return metadata_dictionary