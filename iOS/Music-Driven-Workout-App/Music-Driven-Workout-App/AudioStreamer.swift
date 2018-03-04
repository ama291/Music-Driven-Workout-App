//
//  AudioStreamer.swift
//  Music-Driven-Workout-App
//
//  Created by Larissa Clopton on 3/3/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import Foundation

//class AudioStreamer: NSObject, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate{
//
////    static let shared = AudioStreamer()
////
////    let player:SPTAudioStreamingController
////    let session:SPTSession
////    let auth:SPTAuth
////    let loginUrl: URL?
////
////    override init() {
////        self.player = SPTAudioStreamingController.sharedInstance()
////
////    }
//
//    static let sharedInstance = AudioStreamer()
//    let player = SPTAudioStreamingController.sharedInstance()
//
//    override init() {
//    }
//
//
//}

//class AudioStreamer: NSObject, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
//
//    // MARK: - Shared Instance
//
//    static let sharedInstance = AudioStreamer()
//
//
//    //var player:SPTAudioStreamingController? = SPTAudioStreamingController.sharedInstance()
//    var session:SPTSession = SPTSession()
//    var auth:SPTAuth = SPTAuth.defaultInstance()!
//    var loginUrl: URL?
//
//    // MARK: - Initialization Method
//
//    override init() {
//        let redirectURL = "Music-Driven-Workout-App://returnAfterLogin" // put your redirect URL here
//        auth.redirectURL     = URL(string: redirectURL)
//        auth.clientID        = "8f81031574b54170a24a3a1afab27578"
//        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope]
//        loginUrl = auth.spotifyWebAuthenticationURL()
////        var aplayer = SPTAudioStreamingController.sharedInstance()
////        try! aplayer?.start(withClientId: AudioStreamer.sharedInstance.auth.clientID)
////        self.player = aplayer!
//        super.init()
//    }
//}

