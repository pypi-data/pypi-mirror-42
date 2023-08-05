from copy import deepcopy


def get_node(path, spec, full_path=None):
    key, _, next_path = path.replace('#/', '').partition('/')

    spec_item = spec.get(key)
    if not spec_item:
        raise KeyError('Cannot resolve {}'.format(full_path or path))

    elif not next_path:
        return spec_item

    return get_node(next_path, spec_item, full_path or path)


def resolve(node, spec, ref_map):
    if isinstance(node, dict):
        ref = node.get('$ref')
        if ref:
            cached = ref_map.get(ref)
            if cached:
                return cached

            # Fetch and Cache Resolved Node
            resolved = resolve(get_node(ref, spec), spec, ref_map)
            ref_map[ref] = resolved
            return resolved

        return {key: resolve(val, spec, ref_map) for key, val in node.items()}

    elif isinstance(node, list):
        return [resolve(val, spec, ref_map) for val in node]

    else:
        return node


def resolve_spec(specification):
    resolved = deepcopy(specification)
    reference_map = {}

    for key, val in resolved.items():
        resolved[key] = resolve(val, resolved, reference_map)

    return resolved
