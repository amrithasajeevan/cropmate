from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
import numpy as np
from tensorflow.keras.models import load_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializer import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .models import *
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
import pickle
from django.contrib.auth.hashers import check_password

#Plant Disease Detection


solutions={"0 Apple Scab": "Apple scab is a common disease of plants in the rose family (Rosaceae) that is caused by the ascomycete fungus Venturia inaequalis. While this disease affects several plant genera including Sorbus, Cotoneaster,and Pyrus, it is most commonly associated with the infection of Malus trees, including species of flowering crabapple, as well as cultivated apple. The first symptoms of this disease are found in the foliage, blossoms, and developing fruits of affected trees, which develop dark, irregularly-shaped lesions upon infection. Although apple scab rarely kills its host, infection typically leads to fruit deformation and premature leaf and fruit drop, which enhance the susceptibility of the host plant to abiotic stress and secondary infection. The reduction of fruit quality and yield may result in crop losses of up to 70%, posing a significant threat to the profitability of apple producers. To reduce scab-related yield losses, growers often combine preventive practices, including sanitation and resistance breeding, with reactive measures, such as targeted fungicide or biocontrol treatments, to prevent the incidence and spread of apple scab in their crops.Remove and destroy the fallen leaf litter so that the fungus cannot overwinter. ...Do not overcrowd plants, and make sure the canopy has proper airflow. Fungicide applications at 2-week intervals beginning when new growth is expanding in the spring .The best fungicides available for scab control at this time of the early season are the broad-spectrum protectants: Captan and the EBDCs.",
           "1 Apple Black rot": "Black rot is caused by the fungus Diplodia seriata (syn Botryosphaeria obtusa). The fungus can infect dead tissue as well as living trunks, branches, leaves and fruits. The black rot fungi survive Minnesota winters in branch cankers and mummified fruit (shriveled and dried fruit) attached to the tree.Mancozeb, and Ziram are all highly effective against black rot. Because these fungicides are strictly protectants, they must be applied before the fungus infects or enters the plant. They protect fruit and foliage by preventing spore germination. They will not arrest lesion development after infection has occurred.",
           "2 Apple Cedar Apple rust": "These diseases require plants from two different families in order to complete their life cycle; one plant from the Cupressaceae family (red cedar, juniper) and the other from the Rosaceae family (crabapple, hawthorn, serviceberry). Symptoms are very different on each type of plant.Fungicides with the active ingredient Myclobutanil are most effective in preventing rust. ...Fungicides are only effective if applied before leaf spots or fruit infection appear.Spray trees and shrubs when flower buds first emerge until spring weather becomes consistently warm and dry.Monitor nearby junipers.",
           "3 Apple Healthy": "The Apple Plant is healthy.",
           "4 Cherry healthy": "The Cherry Plant is healthy.",
           "5 Cherry Including Sour Powdery Mildew": "Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) cultivars are commonly affected, rendering them unmarketable due to the covering of white fungal growth on the cherry surface (Fig. 1).You have a choice of low toxicity fungicides like horticultural oils. These include jojoba oil, neem oil, and brand name spray oils designed for fruit trees. Classic fungicides that are used against apple scab, such as sterol inhibitors, are highly effective at controlling powdery mildew.Powdery mildew rarely causes serious damage to its host, but infection by the fungus can discolor leaves, causing those leaves to die and/or drop. Powdery mildew can also infect, disfigure and deform shoots and flowers ",
           "6 Corn Cercospora Leaf Spot Gray leaf spot": "Cercospora Leaf Spot and Gray Leaf Spot are fungal diseases affecting corn crops. Effective management strategies include the application of fungicides with active ingredients such as triazoles and strobilurins, planting resistant varieties, practicing crop rotation, and optimizing tillage practices. Monitoring fields for early symptom detection, maintaining proper nutrient levels, and implementing integrated pest management (IPM) approaches are crucial. Additionally, farmers should consider weather-based predictive models for optimal fungicide application timing. Local agricultural extension services and agronomists can provide region-specific guidance for combating these diseases, emphasizing a holistic approach for sustainable corn cultivation.",
           "7 Corn Common rust": "Common Rust is a fungal disease that can affect corn (maize) plants. This disease is caused by the fungus Puccinia sorghi. Common Rust typically manifests as small, reddish-brown to black pustules or lesions on the upper surfaces of leaves. While Common Rust does not usually cause severe damage to corn plants, heavy infections can lead to reduced photosynthesis and yield losses. Management strategies for Common Rust include planting resistant corn varieties, applying fungicides when necessary, and implementing cultural practices such as crop rotation and maintaining optimal plant spacing. Regular scouting of fields for early symptom detection is crucial for timely intervention. Farmers are advised to consult with local agricultural experts to develop an integrated approach tailored to their specific region and corn cultivation practices",
           "8 Corn Healthy": "The Corn Plant is healthy.",
           "9 Corn Northern Leaf Blight": "Northern Leaf Blight is a common foliar disease affecting corn (maize) plants, caused by the fungus Exserohilum turcicum. This disease is characterized by the development of cigar-shaped lesions on corn leaves, typically starting at the lower leaves and progressing upwards. These lesions are tan to brown, and severe infections can lead to significant yield losses. Effective management strategies for Northern Leaf Blight include planting resistant corn varieties, applying fungicides when necessary, practicing crop rotation, and maintaining proper plant spacing to enhance air circulation. Early detection through regular field monitoring is essential for timely intervention. Farmers are encouraged to consult with local agricultural extension services or agronomists to implement integrated pest management practices tailored to their specific region and corn cultivation practices.",
           "10 Grape Black rot": "Grape Black Rot, caused by the fungus Guignardia bidwellii, poses a threat to grapevines, leading to yield losses and diminished fruit quality. Identified by circular lesions on leaves and black, shriveled berries, this disease can be effectively managed through a combination of strategies. Regular fungicide applications, especially during critical growth stages, prove crucial, with copper-based and systemic fungicides commonly employed. Cultural practices, including pruning infected canes, removing mummified berries, and optimizing canopy management, contribute to reducing disease pressure. Planting resistant grape varieties, timely sanitation to eliminate infected material, and monitoring for symptoms during favorable conditions are integral components of a comprehensive management plan. Collaboration with local agricultural experts and the utilization of weather-based disease forecasting further enhance the ability to tailor strategies for Grape Black Rot control in specific regions.",
           "11 Grape Esca (Black Measles)": "Esca, commonly known as Black Measles, is a complex grapevine disease that can cause significant economic losses in vineyards. It is associated with several pathogens, including Phaeomoniella chlamydospora, Phaeoacremonium spp., and others. Symptoms of Esca include yellowing between leaf veins (chlorosis), wilting, and characteristic tiger-stripe patterns on leaves. In advanced stages, black streaks may appear in the vascular tissue, leading to vine decline. Esca is challenging to control, and preventive measures are crucial. Practices include the use of disease-resistant grape varieties, proper pruning techniques to minimize wounds, and the application of pruning wound protectants. Soil management, cover cropping, and vigilant monitoring for early symptom detection are also part of an integrated approach to Esca management. Consultation with viticulturists and local extension services is essential to develop tailored strategies for mitigating the impact of Esca based on specific vineyard conditions.",
           "12 Grape Healthy": "The Grape Plant is healthy.",
           "13 Grape Leaf Blight (Isariopsis Leaf Spot)": "Grape Leaf Blight, also known as Isariopsis Leaf Spot, is a fungal disease caused by the pathogen Isariopsis viticola. This disease primarily affects grapevines, leading to leaf discoloration and reduced photosynthesis, which can impact fruit quality and yield. Symptoms include small, dark spots on leaves that later develop into larger lesions with distinct margins. As the disease progresses, affected leaves may drop prematurely. Management strategies for Grape Leaf Blight involve a combination of cultural practices and fungicide applications. These may include proper canopy management to improve air circulation, the removal and destruction of infected leaves, and the application of fungicides, especially during periods of high humidity or rain. Additionally, planting disease-resistant grape varieties and monitoring vineyards for early signs of the disease are integral components of an effective management plan. Collaborating with local viticulturists and agricultural experts is crucial for tailoring control measures to specific grape-growing regions and conditions.",
           "14 Peach Bacterial Spot": "Peach Bacterial Spot, caused by the bacterium Xanthomonas arboricola pv. pruni, is a common and economically significant disease affecting peach and other stone fruit trees. Symptoms include small, water-soaked lesions on leaves, fruit, and twigs, which later turn dark and necrotic. Severe infections can lead to defoliation, reduced fruit quality, and economic losses for peach orchards. Management of Peach Bacterial Spot involves a combination of cultural practices, chemical treatments, and resistant cultivar selection. Copper-based bactericides are commonly used during the dormant season to reduce bacterial populations. Pruning and thinning practices that improve air circulation and reduce leaf wetness can help minimize disease spread. Disease-resistant peach varieties are valuable for long-term management. Regular monitoring of orchards for early symptom detection and adherence to integrated pest management (IPM) practices contribute to effective control. Collaboration with local agricultural extension services and horticulturists is essential to develop region-specific strategies for mitigating Peach Bacterial Spot.",
           "15 Peach Healthy": "The Peach Plant is Healthy.",
           "16 Pepper Bell Bacterial Spot": "Bell pepper bacterial spot, caused by Xanthomonas campestris pv. vesicatoria, is a bacterial disease affecting bell pepper plants. Identified by small dark lesions on leaves, this infection can lead to significant yield losses. To manage bell pepper bacterial spot, sanitation practices involve removing infected plant material, and copper-based sprays are applied, particularly during warm and humid conditions. Preventive measures include avoiding overhead irrigation, opting for resistant varieties, and practicing crop rotation. Integrated pest management, emphasizing early detection and a combination of control methods, is crucial. Regular monitoring for symptoms and consultation with local agricultural experts help tailor effective strategies for mitigating bell pepper bacterial spot in specific regions.",
           "17 Pepper Bell Healthy": "The Pepper Bell Plant is healthy.",
           "18 Potato Early Blight": "Potato Early Blight, caused by the fungus Alternaria solani, poses a threat to potato crops with distinctive dark lesions on lower leaves. To manage this disease, farmers employ strategies such as regular fungicide applications, including chlorothalonil or copper-based options, adhering to recommended schedules. Crop rotation, planting resistant varieties, and maintaining proper spacing for improved air circulation contribute to effective control. Timely removal of infected leaves, mulching to prevent soil splashing, and vigilant monitoring for early signs of the disease are integral components of a comprehensive management plan. By integrating these practices, growers can mitigate the impact of Potato Early Blight and protect potato yields.",
           "19 Potato Healthy": "The Potato Plant is healthy.",
           "20 Potato Late Blight": "Potato Late Blight, caused by the oomycete pathogen Phytophthora infestans, is a devastating disease known for its historical impact on potato crops, including the Irish Potato Famine. Late Blight manifests as dark, water-soaked lesions on leaves, stems, and tubers. Under favorable conditions of high humidity and moderate temperatures, the disease can spread rapidly, leading to extensive crop losses. To manage Potato Late Blight, farmers employ a combination of cultural practices and fungicide applications. Strategies include planting disease-resistant potato varieties, practicing crop rotation to reduce inoculum in the soil, and applying fungicides preventatively during periods conducive to disease development. Regular monitoring, early detection, and prompt intervention are crucial to controlling Late Blight and preserving potato yields. Collaborating with local agricultural experts and following integrated pest management (IPM) practices further enhance the effectiveness of control measures.",
           "21 Strawberry Healthy": "The Strawberry Plant id healthy.",
           "22 Strawberry Leaf Scorch": "Strawberry Leaf Scorch is a disease caused by the bacterium Xylella fastidiosa. It primarily affects strawberry plants, causing symptoms such as marginal leaf necrosis, scorched appearance, and leaf discoloration. This bacterium is transmitted by certain leafhoppers, leading to the spread of the disease. To manage Strawberry Leaf Scorch, practices include planting disease-free strawberry plants, controlling insect vectors, and practicing proper sanitation by removing and destroying infected plants. Regular monitoring for symptoms and early detection are crucial for timely intervention. While there are no specific chemical treatments for the bacterium itself, managing the vector population and maintaining overall plant health can help minimize the impact of Strawberry Leaf Scorch. Consulting with local agricultural extension services or plant pathologists is essential for region-specific recommendations and effective disease control strategies.",
           "23 Tomato Bacterial Spot": "Tomato Bacterial Spot, caused by Xanthomonas vesicatoria, poses a threat to tomato plants with characteristic dark, water-soaked lesions on leaves. To manage this bacterial disease, growers implement practices such as sanitation by removing infected plant material and applying copper-based sprays on recommended schedules. Minimizing leaf wetness through appropriate irrigation practices, planting resistant varieties, and adopting crop rotation are key preventive measures. Integrated Pest Management (IPM) strategies, including regular monitoring for early signs and prompt intervention, contribute to effective control. Bacterial Spot can be challenging to manage entirely, making prevention and early detection essential. Collaborating with local agricultural experts provides region-specific guidance for mitigating Tomato Bacterial Spot and preserving tomato yields.",
           "24 Tomato Early Blight": "Tomato Early Blight, caused by the fungus Alternaria solani, poses a challenge to tomato plants with distinct brown lesions on lower leaves. To effectively manage this fungal disease, farmers employ a range of strategies. Regular fungicide applications, featuring active ingredients like chlorothalonil or copper, are implemented, particularly during periods of heightened humidity. Adequate plant spacing, organic mulching to prevent soil splashing, and crop rotation practices contribute to creating an environment less conducive to disease development. Timely removal of infected leaves and the use of resistant tomato varieties further bolster efforts to control Early Blight. With an emphasis on early detection and proactive measures, including consulting with local agricultural experts, growers can implement tailored strategies to mitigate the impact of Tomato Early Blight and protect tomato yields.",
           "25 Tomato Healthy": "The Tomato Plant is Healthy.",
           "26 Tomato Late Blight": "Tomato Late Blight, caused by the pathogen Phytophthora infestans, poses a significant threat to tomato crops, marked by dark lesions and a white, fuzzy growth during humid conditions. To manage this destructive fungal disease, growers employ strategic measures. Regular applications of fungicides with active ingredients like chlorothalonil or copper, especially in high humidity, are essential. Adequate plant spacing, proper ventilation through pruning, and early detection with prompt removal of infected plants contribute to effective control. Minimizing leaf wetness, planting resistant varieties, and adopting crop rotation practices further enhance efforts to mitigate the impact of Tomato Late Blight. Timely intervention and collaboration with local agricultural experts are crucial for tailored strategies and region-specific guidance.",
           "27 Tomato Leaf Mold": "Tomato Leaf Mold, caused by the fungus Passalora fulva, poses a threat to tomato plants with distinctive symptoms like yellowing leaves and olive-green to brownish spore masses on the undersides. To manage this fungal disease, growers employ various strategies. Early-season fungicide applications containing chlorothalonil or copper, combined with proper ventilation through plant spacing and pruning, play a crucial role. Minimizing leaf wetness by adopting drip irrigation, selecting resistant tomato varieties, and promptly removing infected leaves are additional measures to curb Leaf Mold. Cultural practices, including mulching and crop rotation, further contribute to an integrated approach. Regular monitoring for early signs and collaboration with local agricultural experts ensure tailored strategies for effective Tomato Leaf Mold control in specific regions.",
           "28 Tomato Septoria Leaf Spot": "Tomato Septoria Leaf Spot, caused by the fungus Septoria lycopersici, poses a challenge to tomato plants with distinctive circular spots leading to leaf yellowing and defoliation. To effectively manage this fungal disease, growers employ various strategies. Early-season fungicide applications featuring chlorothalonil or copper, along with proper plant spacing and pruning for improved ventilation, are critical. Minimizing leaf wetness through drip irrigation, promptly removing infected leaves, and adopting copper-based sprays contribute to effective control. Planting resistant tomato varieties, implementing cultural practices like mulching, and practicing crop rotation further enhance efforts to curb Septoria Leaf Spot. Regular monitoring for early signs and collaboration with local agricultural experts are essential for tailored strategies and region-specific guidance in effectively managing this common tomato disease.",
           "29 Tomato Spider Mites Two Spotted Spider Mite": "Tomato plants are vulnerable to infestations by the Two-Spotted Spider Mite, causing damage through sap-sucking, stippling, and leaf yellowing. To combat these pests on tomatoes, growers employ various strategies. Regularly hosing down plants with water helps dislodge mites, while maintaining optimal soil moisture creates an unfavorable environment for their proliferation. Introducing predatory mites, such as Phytoseiulus persimilis, serves as a natural control method. Neem oil, known for disrupting mite feeding and reproduction, proves effective as a botanical insecticide. In severe cases, judicious use of miticides may be considered. Additionally, isolating infected plants and pruning heavily infested parts contribute to overall mite management. Vigilant monitoring and early intervention are key to successfully mitigating Two-Spotted Spider Mite infestations, promoting the health of tomato crops.",
           "30 Tomato Target Spot": "Tomato Target Spot, attributed to the fungus Corynespora cassiicola, poses a threat to tomato plants with distinctive circular lesions, giving leaves a target-like appearance. To combat this foliar disease, farmers employ strategic measures. Fungicide applications with chlorothalonil or copper, particularly during periods of high humidity, play a pivotal role. Proper plant spacing and pruning enhance air circulation, creating an environment less favorable for disease development. Minimizing leaf wetness through drip irrigation, coupled with the prompt removal of infected leaves, aids in controlling Target Spot. Cultural practices like mulching and crop rotation further contribute to a comprehensive approach. Selecting tomato varieties resistant or tolerant to Target Spot ensures a proactive defense. Vigilant monitoring and collaboration with local agricultural experts offer valuable guidance for tailored strategies in managing Tomato Target Spot effectively.",
           "31 Tomato Mosaic Virus": "Tomato Mosaic Virus (ToMV) poses a threat to tomato plants, manifesting as mosaic patterns, yellowing, and stunted growth. To manage this viral infection, growers adopt preventive measures. Using certified virus-free seeds or transplants, practicing strict sanitation to avoid contamination, and controlling insect vectors like aphids are crucial strategies. Rapid removal and destruction of infected plants, along with the selection of resistant tomato varieties, contribute to effective management. Additionally, weed control and crop rotation help minimize the risk of virus transmission. While there is no cure for Tomato Mosaic Virus, these proactive measures aid in limiting its impact and preserving the health of tomato crops. Regular monitoring for symptoms and collaboration with agricultural experts offer valuable insights for tailored strategies in managing this viral threat.",
           "32 Tomato Yellow Leaf Curl Virus": "Tomato Yellow Leaf Curl Virus (TYLCV) poses a significant threat to tomato plants, inducing distinct symptoms such as severe leaf yellowing and curling. To combat this viral disease, growers implement strategic measures. Vigorous control of the whitefly vector, Bemisia tabaci, through insecticides and reflective mulches helps disrupt their feeding habits. Opting for tomato varieties resistant or tolerant to TYLCV serves as a crucial preventive step. Prompt removal and destruction of infected plants, along with the use of physical barriers like insect exclusion screens, contribute to minimizing the virus's spread. Early detection of symptoms and collaboration with agricultural experts aid in implementing region-specific strategies for effective TYLCV management. Given the challenging nature of viral diseases, a comprehensive approach that combines preventive measures and vigilant monitoring proves vital in safeguarding the health of tomato crops."
        }

class PlantDiseaseDetectionAPIView(APIView):
    def post(self, request, format=None):
        try:
            # Load your detection model and labels
            # For simplicity, let's assume these variables are defined in your code
            model_path = r'C:\Users\User\cropmate_project\keras_model.h5'
            class_names = list(solutions.keys())  # Use the disease names as class names

            # Load the model
            model = load_model(model_path, compile=False)

            # Get the uploaded image file
            uploaded_file = request.data.get('image_file')

            # Save the image temporarily
            temp_file_path = default_storage.save('temp_image.jpg', ContentFile(uploaded_file.read()))

            # Load the image
            image = Image.open(temp_file_path).convert("RGB")

            # Preprocess the image
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            # Make predictions
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Get the solution for the detected disease
            solution = solutions.get(class_name, "Solution not available")

            # Prepare the response
            response_data = {
                'detected_class': class_name,
                'confidence_score': confidence_score,
                'solution': solution,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Admin login

class SuperuserLoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = SuperuserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            # Using Django's Token model to generate a normal token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'message': "Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or user is not a superuser'}, status=status.HTTP_401_UNAUTHORIZED)


#forgot password

class ForgotPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)

            # Generate a new password
            new_password = generate_random_otp()

            # Update the user's password in the database
            user.set_password(new_password)
            user.save()

            # Send the new password to the user's email
            response = self.send_new_password_to_user_email(user, new_password)
            
            return response
        except ObjectDoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Helper function to send the new password to the user's email
    def send_new_password_to_user_email(self, user, new_password):
        subject = 'New Password'
        message = f'Your new password is: {new_password}'
        from_email = 'ammuluminar123@gmail.com'  # Update with your email
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({'msg': 'New password sent successfully'})
        except BadHeaderError:
            return Response({'msg': 'Invalid header found in the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'msg': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_random_otp():
    return ''.join(random.choices(string.digits, k=6))



#reset password

class ResetPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({'msg': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)

            # Reset password using set_password method
            user.set_password(new_password)
            user.save()

            return Response({'msg': 'Password reset successfully'})
        except ObjectDoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

#Scheme add by admin
        
class SchemeListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Attempt to retrieve the super admin user based on superuser status
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            # Handle the case where the super admin user does not exist
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Set the created_by field to the super admin user ID
        mutable_data['created_by'] = super_admin.id

        serializer = SchemeSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        qs = SchemeAdd.objects.all()
        serializer = SchemeSerializer(qs, many=True)
        return Response(serializer.data)
    

#scheme update by admin
class SchemeUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        a=SchemeSerializer(scheme)
        return Response(a.data)
    def put(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        a=SchemeSerializer(instance=scheme,data=request.data)
        if a.is_valid():
            a.save()
        return Response(a.data)
    def delete(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        scheme.delete()
        return Response({'msg': 'Deleted'})
    


#soil evaluation and crop recomendation 

class CropRecommendationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # loading the saved model and scaler
            model = pickle.load(open(r'C:\Users\User\cropmate_project\cropmateproj\plant_prediction_model', 'rb'))
            scaler = pickle.load(open(r'C:\Users\User\cropmate_project\cropmateproj\plant_prediction_scaler', 'rb'))

            # Extracting data from request
            data = request.data
            N = int(data.get("N"))
            P = int(data.get("P"))
            K = int(data.get("K"))
            temperature = float(data.get("temperature"))
            humidity = float(data.get("humidity"))
            ph = float(data.get("ph"))
            rainfall = float(data.get("rainfall"))

            # Predicting
            input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
            scaled_input = scaler.transform(input_data)
            result = model.predict(scaled_input)[0]

            return Response({"The crop suitable for the condition": result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


#Equipment add by admin
        
class EquipmentListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Attempt to retrieve the super admin user based on superuser status
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            # Handle the case where the super admin user does not exist
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Set the created_by field to the super admin user ID
        mutable_data['created_by'] = super_admin.id

        serializer = EquipementAddSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        qs = EquipmentAdd.objects.all()
        serializer = EquipementAddSerializer(qs, many=True)
        return Response(serializer.data)
    

#Equipment delete,update,retrive
    
from rest_framework.parsers import MultiPartParser, FormParser

class EquipmentUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, **kwargs):
        equipment = EquipmentAdd.objects.get(id=kwargs.get('pk'))
        serializer = EquipementAddSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        equipment = EquipmentAdd.objects.get(id=kwargs.get('pk'))

        # Attempt to retrieve the super admin user based on superuser status
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            # Handle the case where the super admin user does not exist
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Exclude the image field if it is not being updated
        if 'image' not in request.data:
            request.data.pop('image', None)

        # Set the created_by field to the super admin user ID
        request.data['created_by'] = super_admin.id  # Use the ID instead of the username

        serializer = EquipementAddSerializer(instance=equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        equipment = EquipmentAdd.objects.get(id=kwargs.get('pk'))
        equipment.delete()
        return Response({'msg': 'Deleted'})




#farmer/user registration
    
class FarmerRegistrationView(APIView):
    def post(self, request):
        serializer = FarmerRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        qs=CustomUser.objects.all()
        
        a=FarmerRegistrationSerializer(qs,many=True)
        
        return Response(a.data)
    

#login
    
class FarmerLoginView(APIView):
    def post(self, request):
        serializer = FarmerLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user and user.user_type == 'Farmer':
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,'msg': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid credentials or user type'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)