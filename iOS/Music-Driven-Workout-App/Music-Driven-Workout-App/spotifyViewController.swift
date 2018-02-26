//
//  spotifyViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Julia Xu on 2/23/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

//import UIKit
//
//class spotifyViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
//
//    @IBOutlet weak var loginButton: UIButton!
//
//    var auth = SPTAuth.defaultInstance()!
//    var session:SPTSession!
//    var player: SPTAudioStreamingController?
//    var loginUrl: URL?
//
//    override func viewDidLoad() {
//        super.viewDidLoad()
//        setup()
//        NotificationCenter.default.addObserver(self, selector: #selector(spotifyViewController.updateAfterFirstLogin), name: NSNotification.Name(rawValue: "loginSuccessful"), object: nil)
//        // Do any additional setup after loading the view, typically from a nib.
//    }
//
//    func setup () {
//        // insert redirect your url and client ID below
//        let redirectURL = "Music-Driven-Workout-App://returnAfterLogin" // put your redirect URL here
//        //_ = "8f81031574b54170a24a3a1afab27578" // put your client ID here
//        auth.redirectURL     = URL(string: redirectURL)
//        auth.clientID        = "8f81031574b54170a24a3a1afab27578"
//        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope]
//        loginUrl = auth.spotifyWebAuthenticationURL()
//
//    }
//
//    @objc func updateAfterFirstLogin () {
//
//        loginButton.isHidden = true
//        let userDefaults = UserDefaults.standard
//
//        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
//
//            let sessionDataObj = sessionObj as! Data
//            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
//
//            self.session = firstTimeSession
//            initializaPlayer(authSession: session)
//            self.loginButton.isHidden = true
//            // self.loadingLabel.isHidden = false
//        }
//    }
//
//    @objc func initializaPlayer(authSession:SPTSession){
//        print("initialize player")
//        if self.player == nil {
//            print("player nil")
//            self.player = SPTAudioStreamingController.sharedInstance()
//            self.player!.playbackDelegate = self //as SPTAudioStreamingPlaybackDelegate
//            self.player!.delegate = self //as SPTAudioStreamingDelegate
//            try! player?.start(withClientId: auth.clientID)
//            self.player!.login(withAccessToken: authSession.accessToken)
//            print("player initialized")
//        }
//    }
//
//    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
//        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
//        print("logged in")
//        self.player?.playSpotifyURI("spotify:track:58s6EuEYJdlb0kO7awm3Vp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
//            if (error != nil) {
//                print("not playing!")
//            }
//            else {
//                print("playing!")
//            }
//        })
//    }
//
//    @IBAction func loginButtonPressed2(_ sender: Any) {
//        if UIApplication.shared.openURL(loginUrl!) {
//            if auth.canHandle(auth.redirectURL) {
//                // To do - build in error handling
//            }
//        }
//    }
//    @IBAction func loginButtonPressed(_ sender: Any) {
//        if UIApplication.shared.openURL(loginUrl!) {
//            if auth.canHandle(auth.redirectURL) {
//                // To do - build in error handling
//            }
//        }
//    }
//
//
//}

import UIKit

class spotifyViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var player: SPTAudioStreamingController?
    var loginUrl: URL?
    
    @IBOutlet weak var loginButton: UIButton!
    
    @IBAction func loginPressed(_ sender: Any) {
        print("111")
        UIApplication.shared.open(loginUrl!, options: [:], completionHandler: nil)
    }
    
    override func viewDidLoad() {
        print("line 115")
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        setup()
        NotificationCenter.default.addObserver(self, selector: #selector(spotifyViewController.updateAfterFirstLogin), name: NSNotification.Name(rawValue: "loginSuccessfull"), object: nil)
    }
    
    @objc func updateAfterFirstLogin () {
        print("line 122")
        loginButton.isHidden = true
        let userDefaults = UserDefaults.standard
        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
            self.session = firstTimeSession
            print("initializing player")
            initializePlayer(authSession: session)
            print("started init")
        }
    }
    
    func initializePlayer(authSession:SPTSession){
        if self.player == nil {
            self.player = SPTAudioStreamingController.sharedInstance()
            self.player!.playbackDelegate = self
            self.player!.delegate = self
            try! player?.start(withClientId: auth.clientID)
            self.player!.login(withAccessToken: authSession.accessToken)
            print("Player has been initialized")
        }
    }
    
//    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
//        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
//        print("logged in")
//    }
    
    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
        print("logged in")
        self.player?.playSpotifyURI("spotify:track:58s6EuEYJdlb0kO7awm3Vp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
            if (error != nil) {
                print("not playing!")
            }
            else {
                print("playing!")
            }
        })
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setup () {
        // insert redirect your url and client ID below
        let redirectURL = "Music-Driven-Workout-App://returnAfterLogin" // put your redirect URL here
        let clientID = "8f81031574b54170a24a3a1afab27578" // put your client ID here
        auth.redirectURL     = URL(string: redirectURL)
        auth.clientID        = clientID
        // put your scopes here
        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope, SPTAuthUserLibraryReadScope]
        loginUrl = auth.spotifyWebAuthenticationURL()
    }
    
    
}

