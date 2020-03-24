# Voronoi Image Processing

<p align = 'justify'>
A simple python package that allows users to create filtered images using Voronoi diagrams. Here is an example on how to use this package.
</p>


```python
#Load all necessary libraries
from IPython.display import Image as IP_image
from voronoi_image_processing import *

test_image = IP_image(filename = 'MonaLisa.jpg')
display(test_image)
```

    Using TensorFlow backend.



![jpeg](output_2_1.jpeg)



```python
#image is either the name of the iamge or the location of the image.
image = 'MonaLisa.jpg'

#num_cells = number of voronoi cells
#distance  = distance function used to find nearest cell location
#add_boundary = boolean that determines if a cell has a boundary
#alternate    = boolean that determines if every cell is colored or black and white.
params = {'num_cells': 3000, 'distance': 'euclidean', 'add_boundary': True, 'alternate': False}
generate_image_filter(image, **params)
```

    1) Assigning Points To A Cell : 100%|██████████| 2145600/2145600 [00:11<00:00, 191420.60it/s]
    2) Creating A New Filtered Image : 100%|██████████| 3000/3000 [00:09<00:00, 306.26it/s]
    3) Drawing Boundaries (Part 1) : 100%|██████████| 2145599/2145599 [00:07<00:00, 276321.77it/s]
    3) Drawing Boundaries (Part 2) : 100%|██████████| 2145599/2145599 [00:06<00:00, 318701.75it/s]

    0) Prior to Step 1, Ran Nearest Neighbor Algorithm For 7.3 secs
    Enter new image name: NewImageMonaLisa



```python
test_image = IP_image(filename = 'NewImageMonaLisa.jpg')
display(test_image)
```


![jpeg](output_4_0.jpeg)



```python
params = {'num_cells': 500, 'distance': 'euclidean', 'add_boundary': False, 'alternate': False}
generate_face_filter(image, **params)
```

    1) Assigning Points To A Cell For Face 1: 100%|██████████| 113960/113960 [00:00<00:00, 196238.36it/s]
    2) Creating A New Filtered Image For Face 1: 100%|██████████| 500/500 [00:00<00:00, 3232.19it/s]

    0) Prior to Step 1, Ran Nearest Neighbor Algorithm For 0.24 secs on Face 1
    Enter new image name: NewFaceMonaLisa



```python
test_image = IP_image(filename = 'NewFaceMonaLisa.jpg')
display(test_image)
```


![jpeg](output_6_0.jpeg)
