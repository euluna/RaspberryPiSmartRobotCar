# Raspberry Pi Smart Robot Car Project: Computer Vision with OpenCV

This repository documents a university project focused on creating a sign-detecting robot car capable of real-time movement based on visual input. The project utilizes the **Raspberry Pi** platform and the powerful **OpenCV** library to implement complex computer vision tasks.

| Metadata             | Detail                                |
| :------------------- | :------------------------------------ |
| **Project Platform** | Raspberry Pi 3B                       |
| **Project Date**     | April 2021 (Semester 2 Project)       |
| **Student**          | Euluna Gotami                         |
| **Student ID**       | 20113429                              |
| **Course**           | Electrical and Electronic Engineering |

---

## Core Technology and Hardware

The project relies on the **Raspberry Pi** acting as a compact, low-cost computer for on-board image processing, making a traditional CPU too large and impractical. The program was coded using the **OpenCV library in Python 3**, which provides the core of the real-time computer vision functionality for the car.

### Hardware Components

| Component           | Functionality                                                     |
| :------------------ | :---------------------------------------------------------------- |
| **Microcontroller** | Raspberry Pi 3B                                                   |
| **Camera**          | Raspberry Pi Camera Rev 1.3                                       |
| **Motor Driver**    | L298N Motor Driver                                                |
| **Motors**          | 2 x 5V DC Gear Motors                                             |
| **Power**           | 10,000 mAh power bank (for Pi) and 7.4V LiPo battery (for motors) |
| **Control**         | GPIO pins used for motor control (Basic Movement, PWM for speed)  |

<img src="/imgs/car.png" alt="Assembled Raspberry Pi Robot Car" width="400px">

---

## Project Functionalities (Code Overview)

The project included implementation of advanced computer vision tasks such as sign detection, shape counting, face detection, and movement control.

<img src="/imgs/imgDetection.png" alt="Image Detection Process Example" width="400px">

| File Name                  | Functionality            | Computer Vision Method                                                                                                                                                             |
| :------------------------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SignDetectionKMeans.py`   | **Symbol Recognition**   | **HoughCircles** for detection; **K-Means Clustering** to find the dominant color in four image zones to determine direction or 'STOP'.                                            |
| `MoveWithSignDetection.py` | **Autonomous Driving**   | Combines K-Means sign recognition logic with direct **RPi.GPIO** motor controls to make the car move in the detected direction.                                                    |
| `MeasuringDistance.py`     | **Distance Calculation** | **Template Matching** is used to identify the 'measuring distance' symbol. The car starts a timer upon detection and stops it upon seeing a 'STOP' sign to calculate the distance. |
| `FaceRecognition.py`       | **Face Detection**       | Uses the pre-trained **Dlib** model for real-time face detection.                                                                                                                  |
| `ShapeCounting.py`         | **Shape Detection**      | Uses **HSV filtering** and **Contour Approximation** (`arcLength`, `approxPolyDP`) to identify and count shapes (3 sides: triangle, 4 sides: square, >4 sides: circle).            |
| `Movement.py`              | **Basic Movement**       | Core Python script defining motor functions using RPi.GPIO to execute basic movement and move a specified distance (29 cm).                                                        |

### K-Means Sign Detection Flowchart

The sign detection logic relies on capturing a circle using `HoughCircles` and then dividing the area into zones to compare colors.

<img src="/imgs/KMeans%20sign%20detection%20Flowchart.jpg" alt="Flowchart for sign detection using K-Means">

---

## Key Analysis and Learning Outcomes

- **Performance Bottleneck:** The **K-Means** clustering method for sign detection required significant computing power, leading to noticeable **lag** that made it unsuitable for a moving car application.
- **Performance Solution:** **Template Matching** was observed to be faster and required less computing power than K-Means for symbol detection.
- **Image Quality Dependency:** The low quality of the Raspberry Pi Camera resulted in inconsistent symbol readings, which was addressed by using a phone to display the signs, providing its own light source for consistency.
- **Distance Calibration:** Measuring distance relied on calibrating a speed variable via trial and error, as motor movement was observed to be non-linear due to external factors like friction and changing battery voltage.
- **Face Detection Accuracy:** Face detection worked well for most conditions, but struggled when faces were heavily angled due to obscured defining features.
