import cv2
from gui_buttons import Buttons

#initialize buttons
button = Buttons()
button.add_button("person",20,20)
button.add_button("cell phone",20,100)
button.add_button("keyboard", 20, 180)
button.add_button("remote", 20, 260)
button.add_button("scissors", 20, 340)

colors = button.colors



# opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)

#load class list
classes = []
with open("dnn_model/classes.txt","r") as file_object:
        for class_name in file_object.readlines():
            class_name = class_name.strip()
            classes.append(class_name)

print("Object list")
print(classes)

#initialize the camera

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)



#click Function
def click_button(event,x,y,flags,params):
        global button_person
        if event == cv2.EVENT_LBUTTONDOWN:
              button.button_click(x,y)




#create window
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame",click_button)


while True:

        ret, frame = cap.read()


        #get Active button list
        active_buttons = button.active_buttons_list()
        print("Active buttons",active_buttons)

        #object Detection

        (class_ids,scores,bboxes)= model.detect(frame)
        for class_id,score,bbox in zip(class_ids,scores,bboxes):
                (x,y,w,h)=bbox
                class_name = classes[class_id]
                color = colors[class_id]

                if class_name in active_buttons:
                        cv2.putText(frame,class_name,(x,y - 10),cv2.FONT_HERSHEY_PLAIN,2,(200,0,50),2)
                        cv2.rectangle(frame, (x,y),(x+w,y+h),(200,0,50),3)

        # create Button
        #cv2.rectangle(frame,(20,20),(220,70),(0,0,200),-1)



       # print("class_ids",class_ids)
        #print("scores",score)
        #print("bboxes",bboxes)

        # Display Buttons
        button.display_buttons(frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
                break

cap.release()
cv2.destroyAllWindows()
