//
//  LoginViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/23/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import SafariServices
import AVFoundation

struct jsonRequest: Codable {
    var Result: String
    var Status: String
}

var global = Global()

class LoginViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
    // Variables
    var auth = SPTAuth.defaultInstance()!
    
    // Initialzed in either updateAfterFirstLogin: (if first time login) or in viewDidLoad (when there is a check for a session object in User Defaults
    var player: SPTAudioStreamingController?
    var loginUrl: URL?
    
    @IBOutlet weak var loginButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        setup()
        NotificationCenter.default.addObserver(self, selector: #selector(LoginViewController.updateAfterFirstLogin), name: NSNotification.Name(rawValue: "loginSuccessfull"), object: nil)
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setup () {
        // insert redirect your url and client ID below
        let redirectURL = "Music-Driven-Workout-App://returnAfterLogin" // put your redirect URL here
        //_ = "8f81031574b54170a24a3a1afab27578" // put your client ID here
        auth.redirectURL     = URL(string: redirectURL)
        auth.clientID        = "8f81031574b54170a24a3a1afab27578"
        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope]
        loginUrl = auth.spotifyWebAuthenticationURL()
        print(global.userid)
    }
    
    //    func initializaPlayer(authSession:SPTSession){
    //        if self.player == nil {
    //            self.player = SPTAudioStreamingController.sharedInstance()
    //            self.player!.playbackDelegate = self
    //            self.player!.delegate = self
    //            try! player?.start(withClientId: auth.clientID)
    //            self.player!.login(withAccessToken: authSession.accessToken)
    //            print("access token: ")
    //            print(authSession.accessToken)
    //            print("username: ")
    //            print(authSession.canonicalUsername)
    //        }
    //    }
    
    //    func spotifyLogout(authSession:SPTSession) {
    //        self.spotifyLogout(authSession: <#T##SPTSession#>)
    //        print("logged out")
    //    }
    
    func getuseridapi(username: String) {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/getuserid/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, workoutid, key
        let postString = "username=" + username + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                global.userid = json.Result
                print(global.userid)
            }
            
            }.resume()
    }
    
    @objc func updateAfterFirstLogin () {
        
        //        loginButton.isHidden = true
        let userDefaults = UserDefaults.standard
        
        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
            
            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
            
            global.session = firstTimeSession
            // initializaPlayer(authSession: session)
            global.username = session.canonicalUsername
            getuseridapi(username: global.username)
            global.token = global.session.accessToken
            // self.loginButton.isHidden = true
            // self.loadingLabel.isHidden = false
        }
    }
    
    //    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
    //        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
    //        print("logged in")
    //        self.player?.playSpotifyURI("spotify:track:58s6EuEYJdlb0kO7awm3Vp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
    //            if (error == nil) {
    //                print("playing!")
    //            }
    //            if(error != nil) {
    //                print("errors while playing")
    //            }
    //        })
    //    }
    
    
    
    @IBAction func loginButtonPressed(_ sender: Any) {
        if UIApplication.shared.openURL(loginUrl!) {
            
            if auth.canHandle(auth.redirectURL) {
                // To do - build in error handling
            }
        }
    }
    
    
    @IBAction func createNewUser(_ sender:UIButton) {
        if(global.userid != "null") {
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
            present(vc, animated: false, completion: nil)
        } else {
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "newUserID") as! OnboardingViewController
            present(vc, animated: false, completion: nil)
        }
    }
    
}
