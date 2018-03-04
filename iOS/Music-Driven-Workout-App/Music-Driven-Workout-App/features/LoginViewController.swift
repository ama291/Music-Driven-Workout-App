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

class LoginViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
    // Variables
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var userid:String!
    var token:String!
    var username:String!
    
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
        auth.requestedScopes = [SPTAuthStreamingScope, SPTAuthPlaylistReadPrivateScope, SPTAuthPlaylistModifyPublicScope, SPTAuthPlaylistModifyPrivateScope, SPTAuthUserReadPrivateScope, SPTAuthUserLibraryReadScope, SPTAuthUserReadTopScope]
        loginUrl = auth.spotifyWebAuthenticationURL()
        print(userid)
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
                self.userid = json.Result
                print(self.userid)
                
            }
            
            }.resume()
    }
    
    @objc func updateAfterFirstLogin () {
        
        //        loginButton.isHidden = true
        let userDefaults = UserDefaults.standard
        
        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
            
            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
            
            self.session = firstTimeSession
            //            initializaPlayer(authSession: session)
            username = session.canonicalUsername
            getuseridapi(username: username)
            token = session.accessToken
            //            self.loginButton.isHidden = true
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
        
        //     UIApplication.shared.open(loginUrl!, options: nil, completionHandler: nil)
        
        if UIApplication.shared.openURL(loginUrl!) {
            
            if auth.canHandle(auth.redirectURL) {
                // To do - build in error handling
            }
        }
    }
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    //
    //  ViewController.swift
    //  Music-Driven-Workout-App
    //
    //  Created by Alex A on 2/8/18.
    //  Copyright © 2018 UChicago SoftCon. All rights reserved.
    //
    //
    //    @IBOutlet weak var userBox: UITextField!
    //    @IBOutlet weak var passBox: UITextField!
    //    @IBOutlet weak var goButton: UIButton!
    
    //    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    //        if segue.destination is MenuViewController {
    //            let vc = segue.destination as? MenuViewController
    //                vc?.userid = userBox.text!
    //                vc?.username = username
    //                vc?.token = token
    //        }
    //    }
    
    
    //    @IBAction func goButtonClick(_ sender: Any) {
    //        if (userBox.text?.isEmpty)! {
    //            print("ERR: No userid given.")
    //            let alert = UIAlertController(title: "Error", message: "No userid given.", preferredStyle: .alert)
    //            alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
    //                NSLog("The \"OK\" alert occured.")
    //            }))
    //            self.present(alert, animated: true, completion: nil)
    //            return
    //        }
    //        self.performSegue(withIdentifier: "loginSegue", sender: self)
    //    }
    
    @IBAction func createNewUser(_ sender:UIButton) {
        if(userid != "null") {
            //            self.performSegue(withIdentifier: "createnewuser", sender: self)
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
            vc.userid = userid!
            vc.token = token!
            present(vc, animated: false, completion: nil)
        } else {
            //            self.performSegue(withIdentifier: "loginSegue", sender: self)
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "newUserID") as! OnboardingViewController
            //            vc.userid = userid!
            vc.username = username!
            present(vc, animated: false, completion: nil)
        }
    }
    
}
