import software.LEDs as LEDs
import data.simulateUsers.py as simulateUsers



def simulateLookupUser (rfid_data):
## Scans a card then asks the server if the user is registered. Returns boolean value 0/1.
        print("Request: User id lookup. ")
        LEDs.blinkYellow()

        #Lets assume user with card_2_id is a registered user, and that card_1_id is not a user.
        reply = (rfid_data == simulateUsers.card2_id) 

        if reply : 
                print("Found a user match. ")
                return 1
        else :
                print("User not found. ")
                return 0

def simulateRoomUserAccess (user_access):
## Shall not be used in product. Is a simulation tool.
        if user_access :
                print("Access granted. ")
                simulateRoomBehaviour()
        else :
                print("Access denied. ")
                LEDs.blinkRed()


def simulateRoomBehaviour ():
## Shall not be used in product. Is a simulation tool.
        print("Request: Verify/Book room. ")
        reply = 1 # What will the response look like? string, bool?

        if reply :
                print("Room is verified and ready for use. ")
                LEDs.blinkGreen()
                return

        print("Request: Book room. ")
        reply = 1

        if reply :
                print("Room is booked, verified and ready for use. ")
                LEDs.blinkGreen()
        else :
                print("Room is already booked by others. ")
                LEDs.blinkRed()








