// **********************************************************************
//
// Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#ifndef CASINO_ICE
#define CASINO_ICE

module Casino
{
    //
    // A player places bets and then either looses his chips
    // or wins more
    //
    interface Player
    { 
        //
        // The number of chips held by this player
        //
        int getChips();

        //
        // Destroy this player
        //
        ["freeze:write"] void destroy();
    };

    sequence<Player*> PlayerPrxSeq;

    //
    // Thrown when a Player does not have enough chips to place
    // a bet
    //
    exception OutOfChipsException {};

    interface Bet
    {
        //
        // The number of chips each player needs to provide to join
        // this bet
        //
        int getAmount();

        //
        // Player p attempts to accept this bet
        // Raises ObjectNotExistException if the bet is over
        //
        //
        ["freeze:write"] void accept(Player* p) throws OutOfChipsException;
    };

    interface Bank
    {
        //
        // Buy a number of chips for Player p; returns false when player
        // does not exist
        //
        ["freeze:write"] bool buyChips(int chips, Player* p);

        //
        // List of all Players
        //
        PlayerPrxSeq getPlayers();

        //
        // The number of chips sold by this Bank
        //
        int getOutstandingChips();

        //
        // The number of live bets
        //
        int getLiveBetCount();

        //
        // The number of chips earned by the Bank
        //
        int getEarnings();

        //
        // Verify that the total number of chips held by all known players and bets; 
        // match getOutstandingChips();
        //
        ["freeze:read:required"] bool checkAllChips();

        //
        // Create a new bet with the given amount to join; this bet ends in 
        // 'lifetime' milliseconds
        //
        ["freeze:write"] Bet* createBet(int amount, int lifetime);
    };
};

#endif
