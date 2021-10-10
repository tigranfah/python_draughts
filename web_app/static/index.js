let config = {
    orientation: 'black',
    position: 'start',
    draggable: true,
    onDrop: onDrop
};

function make_move(from, to) {
    let move = chess_logic.move({from : from, to : to});
    if (move === null) {
        console.log("Move: " + from + '-' + to + " is invalid");
        return false;
    }
    chess_board.position(chess_logic.fen().split(" ")[0]);
    // $('#moveTable tr:last').after('<tr><td>'+source+'-'+target+'</td><td></td></tr>');
    // $('#moveTable').append($('<tr><td>'+source+'-'+target+'</td><td></td></tr>'))
    return true;
}

function onDrop(source, target, piece) {
    if (!make_move(source, target)) return "snapback";
    request("/move", "POST", chess_logic.fen().split(" ")[0]);
}

function request(route, type, pos) {
    $.ajax({
        url: route,
        type: type,
        data: pos,
        // dataType: 'json',
        success: function(move) {
            make_move(move.substring(0, 2), move.substring(2, 4));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

const chess_logic = new Chess();
const chess_board = Chessboard('myBoard', config);

request("/start", "GET");
