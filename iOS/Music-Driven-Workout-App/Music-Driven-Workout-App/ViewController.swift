//
//  ViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/8/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import SafariServices
import AVFoundation

class ViewController: UIViewController {

    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var player: SPTAudioStreamingController?
    var loginUrl: URL?
    
    @IBOutlet weak var loginButton: UIButton!
    

    func setup () {
        // insert redirect your url and client ID below
        let redirectURL = "" // put your redirect URL here
        let clientID = "8f81031574b54170a24a3a1afab27578" // put your client ID here
        auth.redirectURL     = URL(string: redirectURL)
        auth.clientID        = "8f81031574b54170a24a3a1afab27578"
        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope]
        loginUrl = auth.spotifyWebAuthenticationURL()
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
        NotificationCenter.default.addObserver(self, selector: #selector(ViewController.updateAfterFirstLogin), name: NSNotification.Name(rawValue: "loginSuccessful"), object: nil)
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func initializaPlayer(authSession:SPTSession){
        if self.player == nil {
            self.player = SPTAudioStreamingController.sharedInstance()
            self.player!.playbackDelegate = self as! SPTAudioStreamingPlaybackDelegate
            self.player!.delegate = self as! SPTAudioStreamingDelegate
            try! player?.start(withClientId: auth.clientID)
            self.player!.login(withAccessToken: authSession.accessToken)
        }
    }
    
    @objc func updateAfterFirstLogin () {
        
        loginButton.isHidden = true
        let userDefaults = UserDefaults.standard
        
        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
            
            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
            
            self.session = firstTimeSession
            initializaPlayer(authSession: session)
            self.loginButton.isHidden = true
            // self.loadingLabel.isHidden = false
        }
    }

    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
        print("logged in")
        self.player?.playSpotifyURI("spotify:track:58s6EuEYJdlb0kO7awm3Vp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
            if (error != nil) {
                print("playing!")
            }
        })
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func exerciseTestClicked(_ sender: Any) {
        performSegue(withIdentifier: "exerciseSegue", sender: self)
    }

    @IBAction func loginButtonPressed(_ sender: Any) {
        if UIApplication.shared.openURL(loginUrl!) {
            if auth.canHandle(auth.redirectURL) {
    // To do - build in error handling
            }
        }
    }
}

