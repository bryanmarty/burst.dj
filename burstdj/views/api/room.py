from cornice import Service
from burstdj.core.error import HTTPBadRequest, HTTPConflict, HTTPNotFound, \
    HTTPForbidden

from burstdj.logic import security
from burstdj.logic import room as room_logic
from burstdj.logic.room import RoomAlreadyExists, UserNotInRoom, RoomNotFound

# POST: create a new room
# GET: list all rooms
rooms = Service(
    name='rooms',
    path='/api/room',
    permission='authenticated',
)

# join a room (observe)
room_join = Service(
    name='room_join',
    path='/api/room/{room_id}/join',
    permission='authenticated',
)

# join the queue in a room (actively DJ)
queue_join = Service(
    name='queue_join',
    path='/api/room/{room_id}/queue/join',
    permission='authenticated',
)

# fetch the current activity for a room (poll)
room_activity = Service(
    name='room_activity',
    path='/api/room/{room_id}/activity',
    permission='authenticated',
)

# # fetch the details for a room (this is redundant with activity)
# room = Service(
#     name='room',
#     path='/api/room/{room_id}',
#     permission='authenticated',
# )


@rooms.post()
def post_room(request):
    name = request.json_body.get('name', None)
    if name is None:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        room = room_logic.create_room(name, user_id)
    except RoomAlreadyExists:
        raise HTTPConflict()
    return dict(
        id=room.id,
        name=room.name,
        time_created=room.time_created.isoformat(),
    )

@rooms.get()
def list_rooms(request):
    rooms = room_logic.list_rooms()
    return [
        dict(id=room.id, name=room.name, user_count=room.user_count) for room in rooms
    ]

@room_join.post()
def join_room(request):
    room_id = request.matchdict['room_id']
    try:
        room_id = int(room_id)
    except:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        room = room_logic.join_room(room_id, user_id)
    except RoomNotFound:
        raise HTTPNotFound()
    return dict(
        id=room.id,
        name=room.name,
        users=serialize_users(room.users)
    )


@queue_join.post()
def join_queue(request):
    room_id = request.matchdict['room_id']
    try:
        room_id = int(room_id)
    except:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        newly_joined = room_logic.join_queue(room_id, user_id)
    except UserNotInRoom:
        raise HTTPForbidden()
    except RoomNotFound:
        raise HTTPNotFound()
    return dict(
        success=True,
        newly_joined=newly_joined,
    )


@room_activity.get()
def get_room_activity(request):
    """Return what's going on in this room.  This includes current track
    (most important) and the room's users.
    """
    room_id = request.matchdict['room_id']

    # TODO: fetch current track for room

    # fetch users in room, in order of joining
    users = room_logic.list_room_users(room_id)

    # fetch DJs in room, in order of who will play next
    djs = room_logic.list_room_djs(room_id)

    return dict(
        room_id=room_id,
        current_track=None,
        users=serialize_users(users),
        djs=serialize_users(djs),
    )


def serialize_users(users):
    return [serialize_user(user) for user in users]

def serialize_user(user):
    return dict(id=user.id, name=user.name, avatar=user.avatar_url)