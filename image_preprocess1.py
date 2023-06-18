import cv2, os
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
from multiprocessing import Pool, freeze_support
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from cleanvision import Imagelab
class ImagePreprocessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self._blur_score = 0
        self._normalized_blur_score = 0
        self._blur_threshold = 40

    #Function v1.0.0
    # def set_image_dpi(self, dpi=(300,300)):
    #     image_with_dpi = Image.fromarray(self.gray_image)
    #     image_with_dpi.save(self.image_path, dpi=(dpi, dpi))

    #Function v2.0.0
    def set_image_dpi(self, dpi=(400, 400)):
        image_with_dpi = Image.fromarray(self.gray_image)
        file_name, file_extension = os.path.splitext(self.image_path)
        image_with_dpi.save(file_name+"_processed"+file_extension, dpi=(dpi, dpi))

    def resizeAndPad(self, size, padColor=255):
        h, w = self.gray_image.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw: # shrinking image
            interp = cv2.INTER_AREA

        else: # stretching image
            interp = cv2.INTER_CUBIC

        # aspect ratio of image
        aspect = float(w)/h 
        saspect = float(sw)/sh

        if (saspect > aspect) or ((saspect == 1) and (aspect <= 1)):  # new horizontal image
            new_h = sh
            new_w = np.round(new_h * aspect).astype(int)
            pad_horz = float(sw - new_w) / 2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0

        elif (saspect < aspect) or ((saspect == 1) and (aspect >= 1)):  # new vertical image
            new_w = sw
            new_h = np.round(float(new_w) / aspect).astype(int)
            pad_vert = float(sh - new_h) / 2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        
        # set pad color
        if len(self.gray_image.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
            padColor = [padColor]*3

        # scale and pad
        scaled_img = cv2.resize(self.gray_image, (new_w, new_h), interpolation=interp)
        scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

        return scaled_img

    #check blur function 1.0.0
    def check_blur(self):
        self._blur_score = cv2.Laplacian(self.gray_image, cv2.CV_64F).var()
        return self._blur_score

    #check blur function 2.0.0
    def estimate_blur(self):
        st = time.time()
        #gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gradient_x = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = cv2.addWeighted(cv2.magnitude(gradient_x, gradient_y), 0.5, 0, 0, 0)
        blur_score = cv2.mean(gradient_magnitude)[0]
        et = time.time() - st
        print("Time taken by check Blur function: ", et)
        return blur_score

    #check blur function 3.0.0
   
    def is_blurry2(self):
        imagelab = Imagelab(data_path="",filepaths=[str(self.image_path)])
        issue_types = {"blurry": {}}
        issues = imagelab.find_issues(issue_types)
        imagelab.report()
        #issues = imagelab.find_issues()
        print(issues)
        if issues is not None and issues["blurry"]:
            print("Image is blurry")
            return True
        else:
            print("Image is not blurry")
            return False

    def adjust_brightness(self, value):
        st = time.time()
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
        v = cv2.add(v, value)
        v = np.clip(v, 0, 255)
        hsv[:, :, 2] = v
        self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        et = time.time() - st
        print("Time taken by adjust brightness function: ", et)

    def brightness_level(self):
        average_brightness = int(self.gray_image.mean())
        print("Average brightness level for this image is: ", average_brightness)
        return average_brightness

    def is_image_bright(self, target_range=(125, 255)):
        brightness = self.brightness_level()
        if target_range[0] <= brightness <= target_range[1]:
            print("Image brightness is within the target range.")
            return True
        elif brightness < target_range[0]:
            print("Image is too dark.")
            return False
        else:
            print("Image is too bright.")
            return False
            # brightened_image = cv2.convertScaleAbs(self.image, alpha=1.5, beta=30)
            # return brightened_image

    def adjust_contrast(self, value):
        factor = (value + 127) / 127.0
        self.gray_image = cv2.convertScaleAbs(self.gray_image, alpha=factor, beta=0)

    def check_sharpness(self, threshold=100):
        laplacian = cv2.Laplacian(self.gray_image, cv2.CV_64F)
        sharpness_score = np.mean(np.abs(laplacian))
        return sharpness_score > threshold

    def is_rotated(self):
        height, width = self.gray_image.shape
        if width > height:
            print("Image is rotated!")
            return True
        else:
            return False

    #Not using the function as of now!
    def straighten_image(self):
        if self.is_rotated():
            height, width = self.gray_image.shape
            if width > height:
                print("Rotating image clockwise!")
                self.gray_image = np.rot90(self.gray_image, k=1, axes=(0, 1))  
                plt.imshow(self.gray_image)# Rotate the image data clockwise
                plt.show()
            else:
                print("Rotating image counterclockwise!")
                self.image = np.rot90(self.gray_image, k=3, axes=(0, 1))  # Rotate the image data counterclockwise
                plt.imshow(self.gray_image)# Rotate the image data clockwise
                plt.show()
        return self.gray_image
    
    def check_noise(self):

        # Check for salt-and-pepper noise
        # salt_pepper_noise = self._detect_salt_pepper_noise()
        # if salt_pepper_noise:
        #     self.gray_image = self._remove_salt_and_pepper_noise()

        # Check for Gaussian noise
        #self.gray_image = self._remove_gaussian_noise()
        
        gaussian_time = time.time()
        self.gray_image=self._remove_gaussian_noise()
        print("Time taken to reduce Gaussian noise:",time.time()-gaussian_time)

        # gaussian_time = time.time()
        # self.gray_image = self.remove_poisson_noise_parallel()
        #print("Time taken to reduce Poisson noise:",time.time()-gaussian_time)

        return  self.gray_image
    
    def _remove_poisson_noise(self):
        denoised_image = cv2.fastNlMeansDenoising(self.image, None, h=5)
        return denoised_image
        
    def _remove_poisson_noise_strip(self,image_strip, h, templateWindowSize, searchWindowSize):
        # Convert the image strip to grayscale
        gray_strip = cv2.cvtColor(image_strip, cv2.COLOR_BGR2GRAY)
        
        # Apply the Non-Local Means Denoising algorithm for Poisson noise removal
        denoised_strip = cv2.fastNlMeansDenoising(gray_strip, None, h, templateWindowSize, searchWindowSize)
        
        # Convert the denoised strip back to BGR color space
        denoised_strip = cv2.cvtColor(denoised_strip, cv2.COLOR_GRAY2BGR)
        
        return denoised_strip

    def remove_poisson_noise_parallel(self, h=10, templateWindowSize=7, searchWindowSize=21):
        # Split the image into multiple horizontal strips for parallel processing
        num_cores = multiprocessing.cpu_count()
        rows, cols = self.image.shape[:2]
        strip_height = rows // num_cores
        
        # Create a list of strip indices
        strip_indices = [(i * strip_height, (i + 1) * strip_height) for i in range(num_cores - 1)]
        strip_indices.append(((num_cores - 1) * strip_height, rows))
        
        # Create a process pool executor
        executor = ProcessPoolExecutor(max_workers=num_cores)
        
        # Apply the Non-Local Means algorithm on each image strip in parallel
        futures = []
        for start_row, end_row in strip_indices:
            image_strip = self.image[start_row:end_row, :]
            future = executor.submit(self._remove_poisson_noise_strip, image_strip, h, templateWindowSize, searchWindowSize)
            futures.append(future)
        
        # Get the denoised image strips
        denoised_strips = [future.result() for future in futures]
        
        # Concatenate the denoised image strips
        denoised_image = np.concatenate(denoised_strips, axis=0)
        
        return denoised_image
    
    def apply_wiener_filter(self, kernel_size=3, noise_variance=50):
        # Convert the image to grayscale
        #gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Apply Wiener filter
        filtered = self._apply_wiener_filter_gray(self.gray_image, kernel_size, noise_variance)

        # Merge filtered result back to the original color image
        filtered_image = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)

        return filtered_image

    def _apply_wiener_filter_gray(self,gray_image, kernel_size, noise_variance):
        # Convert the grayscale image to float32
        gray_float32 = np.float32(gray_image)

        # Get the dimensions of the grayscale image
        rows, cols = gray_image.shape

        # Apply DFT
        dft = cv2.dft(gray_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        # Create a Gaussian filter
        gaussian_filter = np.zeros_like(dft_shift, dtype=np.float32)
        crow, ccol = rows // 2, cols // 2
        gaussian_filter[crow - kernel_size:crow + kernel_size, ccol - kernel_size:ccol + kernel_size] = 1

        # Estimate the power spectrum of the image
        spectrum = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) ** 2

        # Expand dimensions for element-wise division
        spectrum_expanded = spectrum[:, :, np.newaxis]

        # Apply the Wiener filter
        wiener_dft = np.divide(gaussian_filter, spectrum_expanded + noise_variance)
        wiener_dft_shifted = np.multiply(dft_shift, wiener_dft)
        wiener_dft_shifted = np.fft.ifftshift(wiener_dft_shifted)
        wiener_output = cv2.idft(wiener_dft_shifted)
        wiener_output = cv2.magnitude(wiener_output[:, :, 0], wiener_output[:, :, 1])

        # Normalize the output
        cv2.normalize(wiener_output, wiener_output, 0, 255, cv2.NORM_MINMAX)
        wiener_output = wiener_output.astype(np.uint8)

        return wiener_output

    def apply_wiener_filter_parallel(self, kernel_size=3, noise_variance=50):
        # Split the image into multiple horizontal strips for parallel processing
        num_cores = multiprocessing.cpu_count()
        rows, cols = self.gray_image.shape[:2]
        strip_height = rows // num_cores

        # Create a list of strip indices
        strip_indices = [(i * strip_height, (i + 1) * strip_height) for i in range(num_cores - 1)]
        strip_indices.append(((num_cores - 1) * strip_height, rows))

        # Create a pool of worker processes
        pool = Pool(processes=num_cores)

        # Apply the Wiener filter on each image strip in parallel
        results = []
        for start_row, end_row in strip_indices:
            image_strip = self.gray_image[start_row:end_row, :]
            result = pool.apply_async(self._apply_wiener_filter_gray, (image_strip, kernel_size, noise_variance))
            results.append(result)

        # Get the filtered image strips
        filtered_strips = [result.get() for result in results]

        # Concatenate the filtered image strips
        filtered_image = np.concatenate(filtered_strips, axis=0)

        return filtered_image

    # Method 2 for removing Gaussian Noise
    def _remove_gaussian_noise(self):
        # Apply Gaussian blur to remove Gaussian noise
        self.gray_image = cv2.GaussianBlur(self.gray_image, (9, 9), 0)
        return self.gray_image 

    def _remove_salt_and_pepper_noise(self, threshold=0.01):
        kernel = np.ones((1, 1), np.uint8)
        self.image = cv2.dilate(self.image, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        self.image = cv2.erode(self.image, kernel, iterations=1)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
        self.image = cv2.medianBlur(self.image, 3)
        return self.image

    def _detect_salt_pepper_noise(self):
        # Count the number of black and white pixels
        num_black = np.sum(self.gray_image == 0)
        num_white = np.sum(self.gray_image == 255)

        # Define thresholds for salt-and-pepper noise detection
        threshold_black = 0.01
        threshold_white = 0.01

        # Determine if salt-and-pepper noise is present
        if num_black / self.gray_image.size > threshold_black or num_white / self.gray_image.size > threshold_white:
            return True
        else:
            return False
    
    #check blur function 4.0.0 (Doesnt work on night-light images)
    def calculate_blur(self):
        # Load the image
        # image = cv2.imread(image_path)

        # # Convert the image to grayscale
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate the gradient magnitude
        gradient_x = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

        # Calculate Laplacian variance
        laplacian = cv2.Laplacian(self.gray_image, cv2.CV_64F)
        laplacian_variance = laplacian.var()

        # Calculate the blur measure using BLIINDS-II formula
        blur_measure = (gradient_magnitude.mean() + laplacian_variance) / 2.0

        # Adaptive thresholding
        threshold = cv2.adaptiveThreshold(self.gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)

        # Count the number of non-zero pixels in the thresholded image
        non_zero_pixels = np.count_nonzero(threshold)

        # Calculate the percentage of non-zero pixels
        nonzero_percentage = non_zero_pixels / (threshold.shape[0] * threshold.shape[1])

        # Check if the image is blurry based on the blur measure and non-zero pixel percentage
        if blur_measure > 100 or nonzero_percentage < 0.1:
            #print("Image is blurry.")
            return True
        else:
            print("Image is not blurry.")
            return False

    def remove_shadow(self):
        rgb_planes = cv2.split(self.image)
        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)
        result = cv2.merge(result_planes)
        result_norm = cv2.merge(result_norm_planes)
        updated_image = result_norm
        cv2.imwrite("Shadow_removed.png",updated_image)
        self.gray_image = cv2.cvtColor(updated_image,cv2.COLOR_BGR2GRAY)

    def binarize_image(self):

        # Apply Otsu's thresholding
        _, binary = cv2.threshold(self.gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        self.gray_image = binary

    def preprocess(self):
        #check if image is rotated.
        if self.is_rotated():
            # st.write("Please upload the image again! Image is rotated.")
            print("Please upload the image again! Image is rotated.")
            return

        #Check for Blur with method 1
        self._blur_score = self.check_blur()
        print("Blur score is: ", self._blur_score)
        if self._blur_score < self._blur_threshold:
            print("Image is blurry. Please recapture the image.")
            return

        #binarize image
        self.binarize_image()

        # Check for noise and apply noise removal
        st =  time.time()
        self.gray_image = self.check_noise()
        et = time.time()-st
        print("Time taken by Noise check function:",et)
       
        #Shadow Removal
        self.remove_shadow()

        #self.gray_image = self.resizeAndPad(size=(1734,2312))  # Obtain the resized image using the given 
        #self.gray_image = self.resizeAndPad(size=(1200,1400))
        self.set_image_dpi(600)


        # Adjust contrast
        self.adjust_contrast(value=70)
        if self.is_image_bright():
            print("Image brightness is within the specified range.")
        else:
            print("Image Brightness levels are not upto the mark. Please recapture the image.")
            return

        # Check for sharpness
        if not self.check_sharpness():
            # Apply sharpening
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.gray_image = cv2.filter2D(self.gray_image, -1, kernel)
        #plt.imshow(self.gray_image)
        #plt.show()
        return self.gray_image

if __name__ == '__main__':
    # Perform the necessary setup for multiprocessing
    freeze_support()
    # Example usage
    image_path ="T:\Python_Tesseract\AWS_Textract\Streamlit_v2\Phone_Images\Pharmeasy_4\Daylight_conditions\IMG20230602095150 - Copy.jpg"
    image_path1 = "T:\Python_Tesseract\AWS_Textract\Streamlit_v2\Image_Processing_Experimental_Codes\Pre-processed-Image.jpg"
    image_path = str(input("Please enter the path of image: "))
    start_time = time.time()
    preprocessor = ImagePreprocessor(image_path1)
    preprocessed_image = preprocessor.preprocess()
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print("Time taken: ",elapsed_time)
    # Display the pre-processed image
    cv2.imwrite("Pre-processed-Image.jpg", preprocessed_image)
