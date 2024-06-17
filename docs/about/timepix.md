# Timepix Detector

Timepix detector uses a scintilator to detect neutrons.
A scintilator is attached to a $45 \degree$ tilted mirror.

## Parameters

Here is the list of parameters that may affect later computational processes.

- Aperture of each lenses
- Gain of the image intensifier
- Photon-to-neutron parameters
  - Minimum number of photons to reconstruct neutrons with
  - Time window of clustering photons
  - Spatial clustering range of photons
- Profile of the scintilator
  - Marker in the scintilator if exist

## Example Experiment set-up with Timepix Detector (June. 2024 @ JParc, SENJU)

### Overview of the detector, sample set-up
  ![IMAGE](timepix_images/overview_timepix.png)

### Preparation
1. Mount detector components on a board.

   <img src="timepix_images/overview_timepix_real.jpeg" width="400">

2. **EXCEPT FOR THE IMAGE INTENSIFIER**, connect powers/communication cables.

    <img src="timepix_images/timepix_cables.JPG" width="400">

3. Block leaking lights

    Make sure there is no leaking light using real-time time-pix monitor.

    You can use `SoPhy` to monitor the image taken by the timepix in real-time.

    <img src="timepix_images/light_leaking_monitor.gif" width="200">

    > `SoPhy` is written by [Amsterdam Scientific Instrument](https://www.amscins.com/)
    > but I couldn't find the documentation online.

    This time, wrapping aluminium tape was enough.

    <img src="timepix_images/light_leaking.png" width="200">

4. Focusing

    Focusing should be done in an order from the time-pix body to the scintilator mount.

    All the apertures should be fully-open at the beginning
    since it is easier to see the effect of focusing when they are wider.

    <img src="timepix_images/focusing.gif" width="200">

    Each group of signals should shrink like the picture above as focusing is optimized.

    <img src="timepix_images/focusing_siemens.png" width="200">

    You can also use a complicated pattern like `Siemens Star` to adjust the focus.

    <img src="timepix_images/taping_lenses.png" width="200">

    Once focusing is done, gently fix the lenses with i.e. aluminium tape.

5. Optimizing image intensifier

    We need to find the intensity saturating points of the image intensifier.

    Use `Zabier` to control the gain of the `image intensifier`.

    **After making sure** that the lens is not exposed to the direct light, plug the power to the `image intensifier`.

    Good starting gain is `0.6` and repeat a measurement until you find the saturating point.

    > Pairwise comparison plot example with fake-data.
    <img src="timepix_images/intensifier_optimization.svg">

    In the example above, since the pair-wise comparison becomes flat at $0.7 V$, we can optimize the intensifier gain around that voltage.

6. Attach scintilator

    Carefully attach the scintilator to the direct lens, that will be facing the beam.

    > Scintilator may move while changing surroundings,
    > i.e. sample, or drift during the measurement for some reason.
    > It can affect the background normalization since scintilator doesn't have a constant spatial efficiency.
    > Secure the scintilator as much as possible once it is mounted as you want.

7. Align with the beam

    Align the center of the lens and scintilator to beam.

    <img src="timepix_images/laser_alignment.jpeg" width="200">

    There should be enough space for a sample and a shield (if applicable).

### Open beam measurement (Background)
Open beam is measured without any samples for background normalization/substration.

### Iron sample measurement (Reference)
Iron sample is measured for bragg edge fitting of the other samples.

### Siemens Star (Spatial Resolution)
Siemens start is used for measuring spatial resolution.

### Sample Measurement (Signal)
This time, a battery sample was measured while charging/resting/decharging.

### Trouble Shooting
- Scintilator
  The scintilator angle is not important as long as it stays the same position throughout the background/signal measurement.
  However, it limited the space to mount a sample rotation station in this experiment.
  The sample couldn't get close enough to the scintilator.
  Therefore we had to use a tilted holder to mount the sample rotating station.

- Detector Component Displacement
  The scintilator was accidentally displaced while mounting the sample.
  Therefore the background image had to be aligned first.
  See [Image Alignment](../user-guide/image_alignment.ipynb) for more detail.
