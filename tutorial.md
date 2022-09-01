Data Plotting tutorial:
In this tutorial we will cover both historical and scaling benchmarks.

This example is used with 10 benchmarks that were performed on a VM in git actions.
We first need to extract the data from the appropriate location, in this case the file a stored at the pytest-benchmark default location: `./.benchmarks/`.
Pytest also adds an intermediate folder named using interpreter information, in this example it was `Linux-CPython-3.10-64bit`, this is handled automatically by the get_paths method.

Getting the paths to the bench folders


```python
from benchmarks.view_utilities import *
from pathlib import Path

#Set the folder containing all the bench files
bench_path = Path('./.benchmarks')

# get the paths to the files
paths = get_paths(bench_path)
latest_path = paths[-1]

print("all paths ", paths)
print("latest path ", latest_path)
```

    all paths  ('.benchmarks/Linux-CPython-3.10-64bit/0001_e318179a3635d6995b3527b037a52234da3ce601_20220826_220324.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_074136.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_075738.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_082003.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_084513.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_090009.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_091731.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_093724.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_095651.json', '.benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_101851.json')
    latest path  .benchmarks/Linux-CPython-3.10-64bit/0001_8882e7c1583de05fe2490e505f020bd678d37fe8_20220830_101851.json


Next, we create the historical dataframe using the list of paths and the dataframe for scaling usisng the latest path.


```python
historical_data = create_dataframe(paths)
historical_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>name</th>
      <th>fullname</th>
      <th>param</th>
      <th>params_size</th>
      <th>params_density</th>
      <th>params_coeftype</th>
      <th>stats_mean</th>
      <th>stats_stddev</th>
      <th>params_dtype</th>
      <th>params_model_solve</th>
      <th>params_operation</th>
      <th>cpu</th>
      <th>datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-function</td>
      <td>test_matmul_QobjEvo_ket[2-dense-function]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-function</td>
      <td>2</td>
      <td>dense</td>
      <td>function</td>
      <td>0.000018</td>
      <td>8.340446e-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz</td>
      <td>2022-08-26 22:06:08.369089</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-array</td>
      <td>test_matmul_QobjEvo_ket[2-dense-array]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-array</td>
      <td>2</td>
      <td>dense</td>
      <td>array</td>
      <td>0.000016</td>
      <td>6.546539e-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz</td>
      <td>2022-08-26 22:06:08.369089</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-string</td>
      <td>test_matmul_QobjEvo_ket[2-dense-string]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-string</td>
      <td>2</td>
      <td>dense</td>
      <td>string</td>
      <td>0.000018</td>
      <td>9.000804e-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz</td>
      <td>2022-08-26 22:06:08.369089</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Matmul_QobjEvo_op@ket-2-sparse-function</td>
      <td>test_matmul_QobjEvo_ket[2-sparse-function]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-sparse-function</td>
      <td>2</td>
      <td>sparse</td>
      <td>function</td>
      <td>0.000018</td>
      <td>7.880117e-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz</td>
      <td>2022-08-26 22:06:08.369089</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Matmul_QobjEvo_op@ket-2-sparse-array</td>
      <td>test_matmul_QobjEvo_ket[2-sparse-array]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-sparse-array</td>
      <td>2</td>
      <td>sparse</td>
      <td>array</td>
      <td>0.000016</td>
      <td>6.363098e-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz</td>
      <td>2022-08-26 22:06:08.369089</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>283</th>
      <td>mesolve-Qubit Spin Chain-8</td>
      <td>test_mesolve[Qubit Spin Chain-8]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain-8]</td>
      <td>Qubit Spin Chain-8</td>
      <td>8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.024849</td>
      <td>1.332601e-02</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>284</th>
      <td>mesolve-Qubit Spin Chain-16</td>
      <td>test_mesolve[Qubit Spin Chain-16]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-16</td>
      <td>16</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.030516</td>
      <td>1.029450e-03</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>285</th>
      <td>mesolve-Qubit Spin Chain-32</td>
      <td>test_mesolve[Qubit Spin Chain-32]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-32</td>
      <td>32</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.055828</td>
      <td>1.924162e-03</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>286</th>
      <td>mesolve-Qubit Spin Chain-64</td>
      <td>test_mesolve[Qubit Spin Chain-64]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-64</td>
      <td>64</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.163021</td>
      <td>3.549377e-03</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>287</th>
      <td>mesolve-Qubit Spin Chain-128</td>
      <td>test_mesolve[Qubit Spin Chain-128]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-128</td>
      <td>128</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.685025</td>
      <td>1.559490e-02</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
  </tbody>
</table>
<p>2880 rows × 14 columns</p>
</div>




```python
scaling_data = json_to_dataframe(latest_path)
scaling_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>name</th>
      <th>fullname</th>
      <th>param</th>
      <th>params_size</th>
      <th>params_density</th>
      <th>params_coeftype</th>
      <th>stats_mean</th>
      <th>stats_stddev</th>
      <th>params_dtype</th>
      <th>params_model_solve</th>
      <th>params_operation</th>
      <th>cpu</th>
      <th>datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-function</td>
      <td>test_matmul_QobjEvo_ket[2-dense-function]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-function</td>
      <td>2</td>
      <td>dense</td>
      <td>function</td>
      <td>0.000031</td>
      <td>0.000012</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-array</td>
      <td>test_matmul_QobjEvo_ket[2-dense-array]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-array</td>
      <td>2</td>
      <td>dense</td>
      <td>array</td>
      <td>0.000029</td>
      <td>0.000037</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Matmul_QobjEvo_op@ket-2-dense-string</td>
      <td>test_matmul_QobjEvo_ket[2-dense-string]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-dense-string</td>
      <td>2</td>
      <td>dense</td>
      <td>string</td>
      <td>0.000030</td>
      <td>0.000026</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Matmul_QobjEvo_op@ket-2-sparse-function</td>
      <td>test_matmul_QobjEvo_ket[2-sparse-function]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-sparse-function</td>
      <td>2</td>
      <td>sparse</td>
      <td>function</td>
      <td>0.000031</td>
      <td>0.000015</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Matmul_QobjEvo_op@ket-2-sparse-array</td>
      <td>test_matmul_QobjEvo_ket[2-sparse-array]</td>
      <td>test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...</td>
      <td>2-sparse-array</td>
      <td>2</td>
      <td>sparse</td>
      <td>array</td>
      <td>0.000027</td>
      <td>0.000014</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Matmul_QobjEvo_op@ket</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>283</th>
      <td>mesolve-Qubit Spin Chain-8</td>
      <td>test_mesolve[Qubit Spin Chain-8]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain-8]</td>
      <td>Qubit Spin Chain-8</td>
      <td>8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.024849</td>
      <td>0.013326</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>284</th>
      <td>mesolve-Qubit Spin Chain-16</td>
      <td>test_mesolve[Qubit Spin Chain-16]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-16</td>
      <td>16</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.030516</td>
      <td>0.001029</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>285</th>
      <td>mesolve-Qubit Spin Chain-32</td>
      <td>test_mesolve[Qubit Spin Chain-32]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-32</td>
      <td>32</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.055828</td>
      <td>0.001924</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>286</th>
      <td>mesolve-Qubit Spin Chain-64</td>
      <td>test_mesolve[Qubit Spin Chain-64]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-64</td>
      <td>64</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.163021</td>
      <td>0.003549</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>287</th>
      <td>mesolve-Qubit Spin Chain-128</td>
      <td>test_mesolve[Qubit Spin Chain-128]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-128</td>
      <td>128</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.685025</td>
      <td>0.015595</td>
      <td>NaN</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
  </tbody>
</table>
<p>288 rows × 14 columns</p>
</div>



Now the data can be sorted by operation, we will also choose to plot only certain operations.
The operations given in the list can be substrings of the actual operation name and are not case sensitive 
(eg: 'matmul' will filter out any operation that doesn't contain matmul in the name)



```python
scaling_operations = ['add','qobjevo','mesolve']
historical_operations = ['matmul']

historical_data = sort_ops(historical_data, historical_operations)

scaling_data = sort_ops(scaling_data, scaling_operations)

print('history: ', historical_data.keys(), '\n scaling: ', scaling_data.keys())
```

    history:  dict_keys(['Matmul_QobjEvo_op@ket', 'Matmul_op@op', 'Matmul_op@ket']) 
     scaling:  dict_keys(['Add', 'Matmul_QobjEvo_op@ket', 'mesolve'])



```python
scaling_data['mesolve']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>name</th>
      <th>fullname</th>
      <th>param</th>
      <th>params_size</th>
      <th>stats_mean</th>
      <th>stats_stddev</th>
      <th>params_model_solve</th>
      <th>params_operation</th>
      <th>cpu</th>
      <th>datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>270</th>
      <td>mesolve-Jaynes-Cummings-4</td>
      <td>test_mesolve[Jaynes-Cummings-4]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-4]</td>
      <td>Jaynes-Cummings-4</td>
      <td>4</td>
      <td>0.028526</td>
      <td>0.002311</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>271</th>
      <td>mesolve-Jaynes-Cummings-8</td>
      <td>test_mesolve[Jaynes-Cummings-8]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-8]</td>
      <td>Jaynes-Cummings-8</td>
      <td>8</td>
      <td>0.030912</td>
      <td>0.000640</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>272</th>
      <td>mesolve-Jaynes-Cummings-16</td>
      <td>test_mesolve[Jaynes-Cummings-16]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-16]</td>
      <td>Jaynes-Cummings-16</td>
      <td>16</td>
      <td>0.046739</td>
      <td>0.001952</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>273</th>
      <td>mesolve-Jaynes-Cummings-32</td>
      <td>test_mesolve[Jaynes-Cummings-32]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-32]</td>
      <td>Jaynes-Cummings-32</td>
      <td>32</td>
      <td>0.110768</td>
      <td>0.004086</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>274</th>
      <td>mesolve-Jaynes-Cummings-64</td>
      <td>test_mesolve[Jaynes-Cummings-64]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-64]</td>
      <td>Jaynes-Cummings-64</td>
      <td>64</td>
      <td>0.349017</td>
      <td>0.006614</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>275</th>
      <td>mesolve-Jaynes-Cummings-128</td>
      <td>test_mesolve[Jaynes-Cummings-128]</td>
      <td>test_solvers.py::test_mesolve[Jaynes-Cummings-...</td>
      <td>Jaynes-Cummings-128</td>
      <td>128</td>
      <td>1.325907</td>
      <td>0.014516</td>
      <td>Jaynes-Cummings</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>276</th>
      <td>mesolve-Cavity-4</td>
      <td>test_mesolve[Cavity-4]</td>
      <td>test_solvers.py::test_mesolve[Cavity-4]</td>
      <td>Cavity-4</td>
      <td>4</td>
      <td>0.028646</td>
      <td>0.009366</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>277</th>
      <td>mesolve-Cavity-8</td>
      <td>test_mesolve[Cavity-8]</td>
      <td>test_solvers.py::test_mesolve[Cavity-8]</td>
      <td>Cavity-8</td>
      <td>8</td>
      <td>0.038817</td>
      <td>0.012263</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>278</th>
      <td>mesolve-Cavity-16</td>
      <td>test_mesolve[Cavity-16]</td>
      <td>test_solvers.py::test_mesolve[Cavity-16]</td>
      <td>Cavity-16</td>
      <td>16</td>
      <td>0.086174</td>
      <td>0.017225</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>279</th>
      <td>mesolve-Cavity-32</td>
      <td>test_mesolve[Cavity-32]</td>
      <td>test_solvers.py::test_mesolve[Cavity-32]</td>
      <td>Cavity-32</td>
      <td>32</td>
      <td>0.336728</td>
      <td>0.010061</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>280</th>
      <td>mesolve-Cavity-64</td>
      <td>test_mesolve[Cavity-64]</td>
      <td>test_solvers.py::test_mesolve[Cavity-64]</td>
      <td>Cavity-64</td>
      <td>64</td>
      <td>1.929214</td>
      <td>0.092705</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>281</th>
      <td>mesolve-Cavity-128</td>
      <td>test_mesolve[Cavity-128]</td>
      <td>test_solvers.py::test_mesolve[Cavity-128]</td>
      <td>Cavity-128</td>
      <td>128</td>
      <td>10.597770</td>
      <td>0.313492</td>
      <td>Cavity</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>282</th>
      <td>mesolve-Qubit Spin Chain-4</td>
      <td>test_mesolve[Qubit Spin Chain-4]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain-4]</td>
      <td>Qubit Spin Chain-4</td>
      <td>4</td>
      <td>0.023840</td>
      <td>0.007519</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>283</th>
      <td>mesolve-Qubit Spin Chain-8</td>
      <td>test_mesolve[Qubit Spin Chain-8]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain-8]</td>
      <td>Qubit Spin Chain-8</td>
      <td>8</td>
      <td>0.024849</td>
      <td>0.013326</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>284</th>
      <td>mesolve-Qubit Spin Chain-16</td>
      <td>test_mesolve[Qubit Spin Chain-16]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-16</td>
      <td>16</td>
      <td>0.030516</td>
      <td>0.001029</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>285</th>
      <td>mesolve-Qubit Spin Chain-32</td>
      <td>test_mesolve[Qubit Spin Chain-32]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-32</td>
      <td>32</td>
      <td>0.055828</td>
      <td>0.001924</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>286</th>
      <td>mesolve-Qubit Spin Chain-64</td>
      <td>test_mesolve[Qubit Spin Chain-64]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-64</td>
      <td>64</td>
      <td>0.163021</td>
      <td>0.003549</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
    <tr>
      <th>287</th>
      <td>mesolve-Qubit Spin Chain-128</td>
      <td>test_mesolve[Qubit Spin Chain-128]</td>
      <td>test_solvers.py::test_mesolve[Qubit Spin Chain...</td>
      <td>Qubit Spin Chain-128</td>
      <td>128</td>
      <td>0.685025</td>
      <td>0.015595</td>
      <td>Qubit Spin Chain</td>
      <td>mesolve</td>
      <td>Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz</td>
      <td>2022-08-30 10:22:06.480975</td>
    </tr>
  </tbody>
</table>
</div>



Now comes param sorting, the fixtures used to make the benchmarks are stored as "param_fixturename", we use these to separate the data into "plots".  

e.g: The Add operation uses "param_density","param_size" and "param_dtype", we use param_sort to make one plot for each value of these parameters:  
plot 1: density=sparse, size= 4, dtype = numpy; plot2: density= dense, size=4, dtype = numpy; etc.   

You can define one parameter as the line_separator, which will draw all values of that parameters on the same plot.  
e.g plot1= density sparse, size =4 and the times for all the dtype appear as differnt colored lines on the plot.

You can also set filters to only keep certain paramter values or exclude a parameter from being used in the sorting.

Only use col_filter for parameters or columns that are not used in the sorting process, such as 'cpu' or 'param_size' in the case of scaling



```python
# Only create plots with sparse density and size 4 or 16
historical_param_filter = {'density': ['sparse'], 'size':[4,16],'model': ['jaynes', 'qubit']}


# delete all entries that contain E5 in the cpu name
col_filter= {'cpu': 'E5'}

# Set the line separator to dtype, coeftype, model_solve or model_steady depending on which operation is being plotted
line_sep = ['type', 'model']

```


```python
historical_data = sort_params(historical_data, line_sep, filters=historical_param_filter, col_filters=col_filter)

# Here we need to exlude param_size from the sorting, as for scaling we will use size on
#  the x axis and thus dont want to separate multiple plots each with a single size value
scaling_data = sort_params(scaling_data, line_sep, filters=None, col_filters=None, exclude=['size'])
```


```python
print(historical_data.keys())
print(historical_data['Matmul_QobjEvo_op@ket-4-sparse'])
```

    dict_keys(['Matmul_QobjEvo_op@ket-4-sparse', 'Matmul_QobjEvo_op@ket-16-sparse', 'Matmul_op@op-4-sparse', 'Matmul_op@op-16-sparse', 'Matmul_op@ket-4-sparse', 'Matmul_op@ket-16-sparse'])
    {'data':                                       group  \
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    9   Matmul_QobjEvo_op@ket-4-sparse-function   
    10     Matmul_QobjEvo_op@ket-4-sparse-array   
    11    Matmul_QobjEvo_op@ket-4-sparse-string   
    
                                              name  \
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    9   test_matmul_QobjEvo_ket[4-sparse-function]   
    10     test_matmul_QobjEvo_ket[4-sparse-array]   
    11    test_matmul_QobjEvo_ket[4-sparse-string]   
    
                                                 fullname              param  \
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    9   test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...  4-sparse-function   
    10  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...     4-sparse-array   
    11  test_lin_alg_QobjEvo.py::test_matmul_QobjEvo_k...    4-sparse-string   
    
        params_size params_density params_coeftype  stats_mean  stats_stddev  \
    9             4         sparse        function    0.000018  7.437344e-07   
    10            4         sparse           array    0.000016  6.910422e-07   
    11            4         sparse          string    0.000018  7.415609e-07   
    9             4         sparse        function    0.000018  6.629470e-07   
    10            4         sparse           array    0.000016  9.226144e-07   
    11            4         sparse          string    0.000018  8.205797e-07   
    9             4         sparse        function    0.000017  8.560437e-07   
    10            4         sparse           array    0.000015  6.367590e-07   
    11            4         sparse          string    0.000017  8.469310e-07   
    9             4         sparse        function    0.000017  6.054093e-07   
    10            4         sparse           array    0.000015  5.312093e-07   
    11            4         sparse          string    0.000016  6.264487e-07   
    9             4         sparse        function    0.000017  1.007945e-06   
    10            4         sparse           array    0.000016  6.407863e-07   
    11            4         sparse          string    0.000017  7.349346e-07   
    9             4         sparse        function    0.000021  9.139363e-07   
    10            4         sparse           array    0.000019  6.992823e-07   
    11            4         sparse          string    0.000021  9.012149e-07   
    9             4         sparse        function    0.000020  1.644778e-06   
    10            4         sparse           array    0.000018  1.714169e-06   
    11            4         sparse          string    0.000020  1.465850e-06   
    9             4         sparse        function    0.000021  2.025465e-05   
    10            4         sparse           array    0.000020  3.078484e-05   
    11            4         sparse          string    0.000021  1.625193e-05   
    
             params_operation                                             cpu  \
    9   Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    9   Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    9   Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket  Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz   
    9   Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    10  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    11  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    9   Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    10  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    11  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz   
    9   Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    9   Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    9   Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    10  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    11  Matmul_QobjEvo_op@ket   Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
    
                         datetime  
    9  2022-08-26 22:06:08.369089  
    10 2022-08-26 22:06:08.369089  
    11 2022-08-26 22:06:08.369089  
    9  2022-08-30 07:44:24.548546  
    10 2022-08-30 07:44:24.548546  
    11 2022-08-30 07:44:24.548546  
    9  2022-08-30 08:22:45.689695  
    10 2022-08-30 08:22:45.689695  
    11 2022-08-30 08:22:45.689695  
    9  2022-08-30 08:48:17.398441  
    10 2022-08-30 08:48:17.398441  
    11 2022-08-30 08:48:17.398441  
    9  2022-08-30 09:03:13.518910  
    10 2022-08-30 09:03:13.518910  
    11 2022-08-30 09:03:13.518910  
    9  2022-08-30 09:20:40.538682  
    10 2022-08-30 09:20:40.538682  
    11 2022-08-30 09:20:40.538682  
    9  2022-08-30 09:40:27.989875  
    10 2022-08-30 09:40:27.989875  
    11 2022-08-30 09:40:27.989875  
    9  2022-08-30 09:59:52.264213  
    10 2022-08-30 09:59:52.264213  
    11 2022-08-30 09:59:52.264213  , 'line_sep': 'params_coeftype'}



```python
print(scaling_data.keys())
print(scaling_data['mesolve'])
```

    dict_keys(['Add-dense', 'Add-sparse', 'Matmul_QobjEvo_op@ket-dense', 'Matmul_QobjEvo_op@ket-sparse', 'mesolve'])
    {'data':                             group                                name  \
    270     mesolve-Jaynes-Cummings-4     test_mesolve[Jaynes-Cummings-4]   
    271     mesolve-Jaynes-Cummings-8     test_mesolve[Jaynes-Cummings-8]   
    272    mesolve-Jaynes-Cummings-16    test_mesolve[Jaynes-Cummings-16]   
    273    mesolve-Jaynes-Cummings-32    test_mesolve[Jaynes-Cummings-32]   
    274    mesolve-Jaynes-Cummings-64    test_mesolve[Jaynes-Cummings-64]   
    275   mesolve-Jaynes-Cummings-128   test_mesolve[Jaynes-Cummings-128]   
    276              mesolve-Cavity-4              test_mesolve[Cavity-4]   
    277              mesolve-Cavity-8              test_mesolve[Cavity-8]   
    278             mesolve-Cavity-16             test_mesolve[Cavity-16]   
    279             mesolve-Cavity-32             test_mesolve[Cavity-32]   
    280             mesolve-Cavity-64             test_mesolve[Cavity-64]   
    281            mesolve-Cavity-128            test_mesolve[Cavity-128]   
    282    mesolve-Qubit Spin Chain-4    test_mesolve[Qubit Spin Chain-4]   
    283    mesolve-Qubit Spin Chain-8    test_mesolve[Qubit Spin Chain-8]   
    284   mesolve-Qubit Spin Chain-16   test_mesolve[Qubit Spin Chain-16]   
    285   mesolve-Qubit Spin Chain-32   test_mesolve[Qubit Spin Chain-32]   
    286   mesolve-Qubit Spin Chain-64   test_mesolve[Qubit Spin Chain-64]   
    287  mesolve-Qubit Spin Chain-128  test_mesolve[Qubit Spin Chain-128]   
    
                                                  fullname                 param  \
    270   test_solvers.py::test_mesolve[Jaynes-Cummings-4]     Jaynes-Cummings-4   
    271   test_solvers.py::test_mesolve[Jaynes-Cummings-8]     Jaynes-Cummings-8   
    272  test_solvers.py::test_mesolve[Jaynes-Cummings-16]    Jaynes-Cummings-16   
    273  test_solvers.py::test_mesolve[Jaynes-Cummings-32]    Jaynes-Cummings-32   
    274  test_solvers.py::test_mesolve[Jaynes-Cummings-64]    Jaynes-Cummings-64   
    275  test_solvers.py::test_mesolve[Jaynes-Cummings-...   Jaynes-Cummings-128   
    276            test_solvers.py::test_mesolve[Cavity-4]              Cavity-4   
    277            test_solvers.py::test_mesolve[Cavity-8]              Cavity-8   
    278           test_solvers.py::test_mesolve[Cavity-16]             Cavity-16   
    279           test_solvers.py::test_mesolve[Cavity-32]             Cavity-32   
    280           test_solvers.py::test_mesolve[Cavity-64]             Cavity-64   
    281          test_solvers.py::test_mesolve[Cavity-128]            Cavity-128   
    282  test_solvers.py::test_mesolve[Qubit Spin Chain-4]    Qubit Spin Chain-4   
    283  test_solvers.py::test_mesolve[Qubit Spin Chain-8]    Qubit Spin Chain-8   
    284  test_solvers.py::test_mesolve[Qubit Spin Chain...   Qubit Spin Chain-16   
    285  test_solvers.py::test_mesolve[Qubit Spin Chain...   Qubit Spin Chain-32   
    286  test_solvers.py::test_mesolve[Qubit Spin Chain...   Qubit Spin Chain-64   
    287  test_solvers.py::test_mesolve[Qubit Spin Chain...  Qubit Spin Chain-128   
    
         params_size  stats_mean  stats_stddev params_model_solve  \
    270            4    0.028526      0.002311    Jaynes-Cummings   
    271            8    0.030912      0.000640    Jaynes-Cummings   
    272           16    0.046739      0.001952    Jaynes-Cummings   
    273           32    0.110768      0.004086    Jaynes-Cummings   
    274           64    0.349017      0.006614    Jaynes-Cummings   
    275          128    1.325907      0.014516    Jaynes-Cummings   
    276            4    0.028646      0.009366             Cavity   
    277            8    0.038817      0.012263             Cavity   
    278           16    0.086174      0.017225             Cavity   
    279           32    0.336728      0.010061             Cavity   
    280           64    1.929214      0.092705             Cavity   
    281          128   10.597770      0.313492             Cavity   
    282            4    0.023840      0.007519   Qubit Spin Chain   
    283            8    0.024849      0.013326   Qubit Spin Chain   
    284           16    0.030516      0.001029   Qubit Spin Chain   
    285           32    0.055828      0.001924   Qubit Spin Chain   
    286           64    0.163021      0.003549   Qubit Spin Chain   
    287          128    0.685025      0.015595   Qubit Spin Chain   
    
        params_operation                                        cpu  \
    270          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    271          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    272          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    273          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    274          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    275          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    276          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    277          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    278          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    279          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    280          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    281          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    282          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    283          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    284          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    285          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    286          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    287          mesolve  Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz   
    
                          datetime  
    270 2022-08-30 10:22:06.480975  
    271 2022-08-30 10:22:06.480975  
    272 2022-08-30 10:22:06.480975  
    273 2022-08-30 10:22:06.480975  
    274 2022-08-30 10:22:06.480975  
    275 2022-08-30 10:22:06.480975  
    276 2022-08-30 10:22:06.480975  
    277 2022-08-30 10:22:06.480975  
    278 2022-08-30 10:22:06.480975  
    279 2022-08-30 10:22:06.480975  
    280 2022-08-30 10:22:06.480975  
    281 2022-08-30 10:22:06.480975  
    282 2022-08-30 10:22:06.480975  
    283 2022-08-30 10:22:06.480975  
    284 2022-08-30 10:22:06.480975  
    285 2022-08-30 10:22:06.480975  
    286 2022-08-30 10:22:06.480975  
    287 2022-08-30 10:22:06.480975  , 'line_sep': 'params_model_solve'}


We can now set a path to store the plots in a create them!


```python
plot_path= Path("images")
# parameters: data, x axis, y axis, x_log, y_log, path
plot_data(historical_data, "datetime", "stats_mean", False, True, path=plot_path)
plot_data(scaling_data, "size", "stats_mean", False, True, path=plot_path)

```


