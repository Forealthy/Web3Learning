// SPDX-License-Identifier: MIT
pragma solidity 0.4.20;

//How to read a code quickly?
contract Election {
    // Model a Candidate
    struct Candidate {
        uint id;
        string name;
        uint voteCount; // amout of people who approve of it
    }

    // Store accounts that have voted
    mapping(address => bool) public voters;
    // Store Candidates
    // Fetch Candidate
    mapping(uint => Candidate) public candidates;
    // Store Candidates Count, NO.x of a list
    uint public candidatesCount;

    // voted event
    event votedEvent ( 
        uint indexed _candidateId 
    );
    // _candidateId is NO.x of a candidate list
    // parameters are those should be wrapped in logs

    function Election () public {
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
    }

    function addCandidate (string _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function vote (uint _candidateId) public {
        // require that they haven't voted before
        require(!voters[msg.sender]);

        // require a valid candidate
        require(_candidateId > 0 && _candidateId <= candidatesCount);

        // record that voter has voted
        voters[msg.sender] = true;

        // update candidate vote Count
        candidates[_candidateId].voteCount ++;

        // trigger voted event
        votedEvent(_candidateId);
    }
}