# Frequency Filtering
## Background info
Frequency filtering allows us to eliminate unwanted frequencies, giving us humans the ability to remove unwanted periodic noise from an image and therefore allowing us to extract information that was previously obscured by the noise. In order to view and pinpoint where these frequencies are, we made use of the Fourier Transform algorithm to translate our image into the frequency domain. The Fourier Transform is a concept developed by Joseph Fourier stating that any continuous periodic signal can be expressed as a summation of sine and cosine waves, each of a different amplitudes. It serves as an important image processing tool, whereby we transform the pixel values of the input image into a heatmap of the corresponding image in the frequency domain. In the resulting Fourier domain image each pixel represents a particular frequency contained in the spatial domain image. Applying the Fourier Transform allows us, among other things, to do image analysis and frequency filtering, as we have illustrated in our project.
## Objective
Our objective was to create a graphical application that would allow a user to filter images by frequency using filter functions in order to remove periodic noise from the images.
Fourier Transformation
Something about the FT function(s): Mihir/Max
We tested three implementations of the Fourier Transform: Numpy built-in, a custom fast fourier transform algorithm, and a naive Python+Numpy implementation. Ultimately, we decided to utilize the built-in Numpy implementation due to simplicity and its speed. A comparison of algorithm running times for a 256x256 grayscale image is provided below:
## Filters
We created four filter functions: gaussian, butterworth, notch, and ideal. For each filter, we implemented the ability to select filter variations, e.g. whether the filter constructed a circle or a band pass, as well as high or low pass.
#### Ideal
Ideal filters allow a desired frequency range to pass through while attenuating an unwanted frequency range, completely eliminate undesired frequencies. Our implementation of this filter is based on the distance of a given coordinate from the origin of the frequency domain. If the coordinate is further from the origin than the frequency cut off, the frequency at that coordinate is eliminated.
#### Gaussian
Gaussian filters selectively remove frequencies according to a gaussian distribution. Given the formula, we know that the variance is inversely proportional to the amount of filtering we wish to apply; the smaller the value of cut off, the higher the frequencies that are suppressed and vice versa. Using this filter, we do not completely eliminate an unwanted frequency; instead, the gaussian filter diminishes their influence, allowing part of the remaining frequencies to  appear in the resulting images.
#### Butterworth
Butterworth filters are designed to have a smooth transition between a flat high frequency to a flat low frequency. Like the gaussian filter, butterworth filters do not completely eliminate all frequencies outside of their cutoff region, but simply diminish their presence.
#### Notch
Notch filters are used to target specific points of the frequency domain to eliminate unwanted frequencies without eliminating an entire spectrum. The notch filter we used was an ideal notch filter; given a point in the frequency domain, this filter passes frequencies in the surrounding area that are within the cutoff frequency range.
#### Low Pass / High Pass Variants
For our filter functions, we have been describing their low pass aspects. Their high pass qualities will allow higher frequencies to pass through the filter; for an ideal filter, this means that frequencies that are further from the origin will pass, while frequencies that are within the given frequency range will not.
#### Band Variants
Bandpass filters allow a small band of frequencies to pass through the filter. They can eliminate both low and high frequencies, allowing only mid range frequencies to pass. Bandstop filters do the opposite, eliminating mid range frequencies.
#### Directional Filtering
Directional filters select frequencies of an image that are oriented in a particular direction. We combine the directional filter with other band filtering in order to create a directional band filter.
## Software Design
For the creation of our application, we applied the Model-view-adapter (MVA) architectural pattern. The MVA separates the data (or the model) from the user interface (or the view), allowing for efficiency and modularity, as changes in the user interface do not interfere with data handling and vice versa. This is accomplished by a linear relationship between the model and the view, mediated by the controller (or adapter).
As per the MVA pattern, the application is split into three main abstraction layers: the QtGUI class acting as the view, the FrequencyFilteringApp class acting as the adapter, and the Filter class acting as the model. The Fourier Transform module is implemented as an additional fourth abstraction layer (interfacing directly with the adapter), and provides the different algorithms to compute the 2D discrete Fourier Transform.
#### View: QtGUI Class
The QtGUI class defines the layout and presentation of the application, such as the input image, its DFT, the masked DFT, the resulting filtered image, as well as controls for the user to choose which filter to use and their corresponding parameters.
The main window view contains two sub-views: the left containing four images defined by the QImageGrid class, the right containing a panel with controls for user input of filter values defined by the QControlPanel class. In addition, the QControlPanel class utilizes several of a custom slider-spinbox widget combination, called the QSpinSlider class. This allows users to drag the slider to change filter values in addition to typing a value directly or clicking increment/decrement buttons.
We chose Qt as our GUI framework because it is a modern, cross-platform software framework that is object oriented and has detailed documentation. Its ready-made UI elements and native widgets allow for an effective realization of our project objective. 
#### Adapter: FrequencyFilteringApp Class
Following the adapter pattern, the FrequencyFilteringApp class acts as the mediator between the GUI and the data model, as well as providing the entry point for the application. Upon initialization, the adapter creates a single instance of the GUI and the Filters classes. It then binds its own methods to the view’s event handlers.
When a user makes a change to any of the filter parameters or selects a new image, the view event handler calls the appropriate adapter method bound by the adapter. This method effectively translates (adapts) the user action into the required change to the data model, but leaves the implementation of that change up to the data model.
Once the data model is updated, the adapter recomputes the masked DFT and result image and passes this information back to the view to be displayed.
#### Model: Filters Class
The Filters class generates filter masks that are later applied to the frequency domain of the image. These masks are customized based on the parameters given and the filter type: ideal, gaussian, butterworth, or notch. Bandpass and bandstop variants are also available options, as are low and high pass variants. A directional filter can be applied to any of these masks, allowing the user to specify specific frequencies to be passed or eliminated.
Since the user is able to adjust filter values and view results in real-time, the Strategy pattern was applied to handle the implementation of the inputted data as it is passed to Filter by the Controller. Strategy allows Filter, which contains definitions for each of the filter functions, to select the appropriate algorithm at runtime based on the user’s input.
## Further Implementation
Things that could be further implemented for increased functionality, given additional time:
* The ability to save/export the resulting image
* Node editor for more complex mask creation

## References
* http://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
* https://en.wikipedia.org/wiki/Model–view–adapter
* https://en.wikipedia.org/wiki/Strategy_pattern
