//
//  WorkSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkSummaryViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {

    var userid: String!
    var themes: String!
    var categories: String!
    var musclegroup: String!
    var equipment: String!
    var duration: String!
    var difficulty: String!
    var token: String!
    var username: String!
    
    //spotify
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var player: SPTAudioStreamingController?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    @objc func updateAfterFirstLogin () {
        
//        loginButton.isHidden = true
        let userDefaults = UserDefaults.standard
        
        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
            
            let sessionDataObj = sessionObj as! Data
            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
            
            self.session = firstTimeSession
            initializaPlayer(authSession: session)
            username = session.canonicalUsername
            token = session.accessToken
//            self.loginButton.isHidden = true
            // self.loadingLabel.isHidden = false
        }
    }
    
    func audioStreamingDidLogin(_ audioStreaming: SPTAudioStreamingController!) {
        // after a user authenticates a session, the SPTAudioStreamingController is then initialized and this method called
        print("logged in")
        self.player?.playSpotifyURI("spotify:track:58s6EuEYJdlb0kO7awm3Vp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
            if (error == nil) {
                print("playing!")
            }
            if(error != nil) {
                print("errors while playing")
            }
        })
    }
    
    @IBAction func startMusic(_ sender: UIButton) {
        print("workoutsummary")
        print("username")
        print(username)
        print("access token")
        print(token)
        updateAfterFirstLogin()
    }
    
    func initializaPlayer(authSession:SPTSession){
        if self.player == nil {
            self.player = SPTAudioStreamingController.sharedInstance()
            self.player!.playbackDelegate = self
            self.player!.delegate = self
            try! player?.start(withClientId: auth.clientID)
            self.player!.login(withAccessToken: authSession.accessToken)
            print("access token: ")
            print(authSession.accessToken)
            print("username: ")
            print(authSession.canonicalUsername)
        }
    }
    
    func playPauseSong(player:SPTAudioStreamingController){
//        if player.isPlaying == true {
//            player.setIsPlaying(false, callback: nil)
//        }else{
//            player.setIsPlaying(true, callback: nil)
//        }
        player.setIsPlaying(<#T##playing: Bool##Bool#>, callback: <#T##SPTErrorableOperationCallback!##SPTErrorableOperationCallback!##(Error?) -> Void#>)
    }
    
    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didChangePlaybackStatus isPlaying: Bool) {
        self.player?.queueSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", callback: {(error) in
            if (error == nil) {
                print("queued!")
            } else {
                print("error queueing")
            }
        })
    }

}
