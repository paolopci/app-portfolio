import pandas as pd


df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        # sovrascrive il file CSV in modo che lo stato aggiornato
        #  resti valido fra esecuzioni diverse del programma.
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """
            df.loc[df["id"] == self.hotel_id, "available"]
            Si sta selezionando la colonna available solo per le righe in cui 
            la colonna id è uguale a self.hotel_id.
        """
        availability = df.loc[df["id"] ==
                              self.hotel_id, "available"]  # filtro su id
        print(availability)
        # Accedere all’elemento con availability.iloc[0] per fare un
        # confronto esplicito con "yes"
        if not availability.empty and availability.iloc[0] == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
                    Thanl you for you reservation!
                    Here are you booking data:
                    Name: {self.customer_name}
                    Hotel name: {self.hotel.name}
                """
        return content


# main program -------------------------------
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_ticket = ReservationTicket(
        customer_name=name, hotel_object=hotel)
    print(reservation_ticket.generate())
else:
    print("Hotel is not free.")
