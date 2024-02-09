import face_recognition as fr 
import numpy as np 
from profiles.models import Profile

def is_ajax(request):
    # Check if the request is AJAX
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def get_encoded_faces():
    """
    This function loads all user profile images and encodes their faces.
    """
    # Retrieve all user profiles from the database 
    qs = Profile.objects.all()

    # Create a dictionary to hold the encoded face for each user
    encoded = {}

    for p in qs:
        # Initialize the encoding variable with None
        encoding = None

        # Load the user's profile image
        face = fr.load_image_file(p.photo.path)

        # Encode the face (if detected)
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print("No face found in the image")

        # Add the user's encoded face to the dictionary if encoding is not None
        if encoding is not None:
            encoded[p.user.username] = encoding

    # Return the dictionary of encoded faces
    return encoded

def classify_face(img):
    """
    This function takes an image as input and returns the name of the recognized face.
    """
    # Load all the known faces and their encodings
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    # Load the input image
    img = fr.load_image_file(img)

    try:
        # Find the locations of all faces in the input image
        face_locations = fr.face_locations(img)

        # Encode the faces in the input image
        unknown_face_encodings = fr.face_encodings(img, face_locations)

        # Identify the faces in the input image
        face_names = []
        for face_encoding in unknown_face_encodings:
            # Compare the encoding of the current face to the encodings of all known faces
            matches = fr.compare_faces(faces_encoded, face_encoding)

            # Find the known face with the closest encoding to the current face
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            # If the closest known face is a match for the current face, assign the name
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        # Return the name of the first recognized face in the input image
        return face_names[0]
    except:
        # If no faces are found in the input image or an error occurs, return False
        return False






""" import face_recognition as fr 
import numpy as np 
from profiles.models import Profile

def is_ajax(request):
    return request.headers.get('x-requested-with') 'XMLHttpRequest'

def get_encoded_faces():

    # this function loads all user profile images and encodes their faces


    # Retrieve all user profiles from the database 

    qs = Profile.objects.all()

    # Create a dictionary to hold the encoded face for each user encoded = {}
    encoded = {}

    for p in qs:
        # Initialize the encoding variable with None

        encoding = None

        #load the user's profile image
        face = fr.load_image_file(p.photo.path)

        #encode the face (if-detected)
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) >0:
            encoding = face_encodings[0]
        else:
            print("no face found in the image")

        #add the users's encoded face to the dictionary if encoding
        if encoding is not None:
            encoded[p.user.username] = encoding

    #return the dictionary of encoded faces
    return encoded


def classify_face(img):
    #this function takes an image as input and returns the name of th

    #load all the known faces and their encodings
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    #load the input image
    img = fr.load_image_file(img)

    try:
        #find the locations of all faces in the input image
        face_locations = fr.face_locations(img)

        #encode the faces in the input image
        unknown_face_encodings = fr.face_encodings(img,face_locations)

        #identify the faces in the input image
        face_names = []
        for face_encoding in unknown_face_encodings:
            #compare the encoding of the current face to the encodi
            matches = fr.compare_faces(faces_encoded, face_encoding)

            #find the known face with the closest encoding to the 
            face_distances = fr.face_distance(faces_encoded, face_en)
            best_match_index = np.argmin(face_distances)

            #if the closest known face is a match for the current 
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        #return the name of the first face in the input image
        return face_names[0]
    except:
        #if no faces are found in the input image or an error occu
        return False




    







 """