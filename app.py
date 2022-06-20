import streamlit as st # for creating webapp
import cv2 # image processing
from PIL import Image, ImageEnhance
import numpy as np # to deal with arrays

def cartoonize_image(our_image):
    new_img = np.array(our_image.convert('RGB'))
    # mask
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(new_img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def cannize_image(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.GaussianBlur(new_img, (9, 9), 0)
    canny = cv2.Canny(img, 100, 150)

    return canny

def main():

    st.title('Image Editing App')
    st.text('Edit your images in a fast and simple way')

    activities = ['Detection', 'About']
    choice = st.sidebar.selectbox('Select Activity', activities)

    if choice == 'Detection':
        st.subheader('Face Detection')
        image_file = st.file_uploader('Upload Image', type=['jpg', 'jpeg', 'png'])

        if image_file is not None:
            our_image = Image.open(image_file)
            st.text('Original Image')
            enhance_type = st.sidebar.radio('Enhance type', \
                                            options=['Gray-scale', 'Contrast', 'Brightness', 'Blurring', 'Sharpness'])
            st.sidebar.image(our_image)

            if enhance_type == 'Gray-scale':
                # convert image to RGB arrays
                img = np.array(our_image.convert('RGB'))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                st.image(gray)

            elif enhance_type == 'Contrast':
                rate = st.sidebar.slider('Contrast', 0.5, 6.0, 2.5)
                enhancer = ImageEnhance.Contrast(our_image)
                enhanced_img = enhancer.enhance(rate)
                st.image(enhanced_img)

            elif enhance_type == 'Brightness':
                rate = st.sidebar.slider('Brightness', 0.5, 6.0, 1.5)
                enhancer = ImageEnhance.Brightness(our_image)
                enhanced_img = enhancer.enhance(rate)
                st.image(enhanced_img)

            elif enhance_type == 'Blurring':
                rate = st.sidebar.slider('Blurring', 0.5, 6.0, 1.5)
                blurred_img = cv2.GaussianBlur(np.array(our_image), (15, 15), rate)
                st.image(blurred_img)

            elif enhance_type == 'Sharpness':
                rate = st.sidebar.slider('Sharpness', 0.5, 6.0, 1.5)
                enhancer = ImageEnhance.Sharpness(our_image)
                enhanced_img = enhancer.enhance(rate)
                st.image(enhanced_img)

            else:
                st.image(our_image)

        tasks = ['Cartoonize', 'Cannize']
        feature_choice = st.sidebar.selectbox('Find features', tasks)

        if st.sidebar.button('Process'):

            if feature_choice == 'Cartoonize':
                result_img = cartoonize_image(our_image)
                st.image(result_img)

            if feature_choice == 'Cannize':
                result_img = cannize_image(our_image)
                st.image(result_img)


    if choice == 'About':
        st.subheader('About the developer')
        st.markdown('Built with streamlit by [Slender](https://huggingface.co/Slender)')
        st.text('My name is Slender, I am computer science student with an experience of 3 years in python programming.')


if __name__ == '__main__':
    main()