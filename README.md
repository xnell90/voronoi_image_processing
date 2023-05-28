# Voronoi Image Processing

<p align = 'justify'>
A simple python package that allows users to create filtered images using Voronoi diagrams. Here is an example on how to use this package.
</p>


```python
#Load all necessary libraries
from IPython.display import Image as IPImage
from voronoi_image_processing import *

test_image = IPImage(filename = 'mona_lisa.jpeg')
display(test_image)
```

    Using TensorFlow backend.



![jpeg](output_2_1.jpeg)



```python
#image is either the name of the iamge or the location of the image.
image = 'mona_lisa.jpeg'

#Before running the function, makes sure it passes in a dicitonary with the following keys:
# num_cells = number of voronoi cells
# distance  = distance function used to find nearest cell location (see sklearn's distance functions)
# add_boundary = boolean that determines if a cell has a boundary
# alternate_cell_color = boolean that determines if every cell is colored or black and white.
# display_new_image = boolean that determines if you want to display the new image after processing
settings = {
    'num_cells': 3000,
    'distance': 'euclidean',
    'add_boundary': True,
    'alternate_cell_color': False,
    'display_new_image': True
}
generate_filtered_image(image, settings)
```

    1) Assigning Points To A Cell : 100%|██████████| 2145600/2145600 [00:10<00:00, 196023.15it/s]
    2) Creating A New Filtered Image : 100%|██████████| 3000/3000 [00:03<00:00, 868.89it/s]
    3) Drawing Boundaries (Part 1) : 100%|██████████| 2145599/2145599 [00:07<00:00, 294257.40it/s]
    3) Drawing Boundaries (Part 2) : 100%|██████████| 2145599/2145599 [00:07<00:00, 298935.74it/s]


    0) Prior to Step 1, Ran Nearest Neighbor Algorithm For 4.34 secs



```python
test_image = IPImage(filename = 'mona_lisa_filtered.jpeg')
display(test_image)
```


![jpeg](output_4_0.jpeg)



```python
settings = {
    'num_cells': 500,
    'distance': 'euclidean',
    'add_boundary': False,
    'alternate_cell_color': False,
    'display_new_image': True
}
generate_filtered_faces(image, settings)
```

    1) Assigning Points To A Cell For Face 1: 100%|██████████| 113960/113960 [00:00<00:00, 211050.75it/s]
    2) Creating A New Filtered Image For Face 1: 100%|██████████| 500/500 [00:00<00:00, 2978.53it/s]


    0) Prior to Step 1, Ran Nearest Neighbor Algorithm For 0.24 secs on Face 1



```python
test_image = IPImage(filename = 'mona_lisa_filtered.jpeg')
display(test_image)
```


![jpeg](output_6_0.jpeg)
