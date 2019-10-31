import axios from 'axios';


function JoinUser(token, socket, io) {
    axios.get('http://bpiapp:8000/auth/users/whoami/', {
        headers: {
            Authorization: `JWT ${token}`,
        },
    }).then((response) => {
        const room = response.data.id;
        socket.join(room);
    }).catch((err) => {
        console.log('error:', err);
    });
}

export default JoinUser;
