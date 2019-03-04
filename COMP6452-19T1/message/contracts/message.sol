pragma solidity ^0.4.17;

contract Message {
    string public message;

    function Message(string initialMessage) public {
        message = initialMessage;
    }
    
    function setMessage(string newMessage) public {
        message = newMessage;
    }
}