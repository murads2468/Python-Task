
from datetime import datetime


class BookingScheduler:
    def __init__(self):
        self.bookings = []
        self.booking_ids = set()

    def add_booking(self, room, start, end, booking_id):
        # Validate datetime objects
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("Start and end must be datetime objects")

        # Validate booking time
        if end <= start:
            raise ValueError("End time must be after start time")

        # Check duplicate booking ID
        if booking_id in self.booking_ids:
            raise ValueError("Duplicate booking ID")

        # Find conflicts in the same room
        conflicts = []

        for booking in self.bookings:
            if booking["room"] == room:
                if start < booking["end"] and end > booking["start"]:
                    conflicts.append(booking)

        # Reject booking if conflicts exist
        if conflicts:
            return {
                "accepted": False,
                "booking_id": booking_id,
                "conflicts": conflicts
            }

        # Accept booking
        new_booking = {
            "room": room,
            "start": start,
            "end": end,
            "booking_id": booking_id
        }

        self.bookings.append(new_booking)
        self.booking_ids.add(booking_id)

        # Keep bookings sorted by room and start time
        self.bookings.sort(
            key=lambda booking: (booking["room"], booking["start"])
        )

        return {
            "accepted": True,
            "booking_id": booking_id,
            "conflicts": []
        }


# Create scheduler
scheduler = BookingScheduler()

# Sample datetime objects
date = datetime(2026, 11, 7)

start1 = date.replace(hour=9, minute=0)
end1 = date.replace(hour=10, minute=0)

start2 = date.replace(hour=10, minute=0)
end2 = date.replace(hour=11, minute=0)

start3 = date.replace(hour=9, minute=30)
end3 = date.replace(hour=10, minute=30)

# Add bookings
print(scheduler.add_booking("Room A", start1, end1, "B001"))
print(scheduler.add_booking("Room A", start2, end2, "B002"))
print(scheduler.add_booking("Room A", start3, end3, "B003"))
