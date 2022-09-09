import pandas as pd
import pytest
import numpy as np
import benchmarks.view_utilities as view


def get_params(length):
    operations = ["add", "matmul", "qobjevo", "mcsolve", "mesolve"]
    times = np.linspace(1, length, length, dtype=int)
    size = np.logspace(1, length, length, base=2, dtype=int)
    density = ["sparse"] * int(length / 2) + ["dense"] * int(length / 2)
    model = ["qubit"] * int(length / 2) + ["cavity"] * int(length / 2)

    return (operations, times, size, density, model)


def get_sum(all_ops, times, filter_ops):
    res = 0
    for i, op in enumerate(all_ops):
        for filter in filter_ops:
            if op == filter:
                res += np.sum(times + i * 10)

    return res


def create_dataframe(params):

    operations, times, size, density, model = params

    result = pd.DataFrame()

    for i, item in enumerate(operations):
        tmp_dict = {}
        tmp_dict["size"] = size.tolist()
        tmp_dict["times"] = (times + i * 10).tolist()
        tmp_dict["params_operation"] = [item] * len(times)
        if "solve" in item:
            tmp_dict["model"] = model
        else:
            tmp_dict["density"] = density
        tmp = pd.DataFrame(tmp_dict)
        result = pd.concat([result, tmp])

    return result


@pytest.fixture(params=np.logspace(1, 8, 8, base=2, dtype=int).tolist())
def length(request):
    return request.param


@pytest.mark.parametrize(
    ["filters"],
    [
        pytest.param(
            (["add"], ["matmul"], ["qobjevo"], ["mcsolve"], ["mesolve"]),
            id="single_filters",
        ),
        pytest.param(
            (["add", "matmul"], ["qobjevo", "mcsolve", "mesolve"]),
            id="multi_filters",
        ),
    ],
)
def test_sort(filters, length):
    params = get_params(length)
    operations, times, _, _, _ = params
    data = create_dataframe(params)

    for filter in filters:

        test_data = view.sort_ops(data, filter)
        ref_time = get_sum(operations, times, filter)

        test_time = 0
        for _, value in test_data.items():
            test_time += value["times"].sum()

        assert filter == list(test_data.keys())
        assert test_time == ref_time
