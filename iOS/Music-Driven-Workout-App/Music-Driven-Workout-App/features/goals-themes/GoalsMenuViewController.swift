//
//  GoalsMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalsMenuViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
//}, UITableViewController {

    var userid: String!
    var tableArray = [String:Any] ()
    var username: String!
    var token: String!
    var player: SPTAudioStreamingController?
    var passedUserId = String()
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var audiostreaming: SPTAudioStreamingController?
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.dataSource = self
        self.tableView.delegate = self
        // Do any additional setup after loading the view.
        populateGoals()
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
    
    struct goalsResult: Codable {
        var Result: String
        var Status: String
    }
    
    func populateGoals() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/goalssaved/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + userid + "&key=SoftCon2018"
        passedUserId = userid
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            guard let content = data else {
                print("not returning data")
                return
            }
//            guard let json = try? JSONDecoder().decode(goalsResult.self, from: data!) else { return }
            guard let json = (try? JSONSerialization.jsonObject(with: content, options: JSONSerialization.ReadingOptions.mutableContainers)) as? [String: Any] else {
                print("Not containing JSON")
                return
            }
//            let jsonRes = json["Result"]!
            if let array = json as? [String : Any] {
                self.tableArray = array
                print(self.tableArray)
            }
            print(self.tableArray)
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
            }.resume()
    }

    
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
 
//extension GoalsMenuViewController {
//    override func
        func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath) as UITableViewCell
        cell.textLabel?.text = (self.tableArray["Result"]! as! String)
        return cell
    }
    
//    override
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        return self.tableArray.count/2
        
    }
    
//    @IBAction func addGoal(_sender: UIButton) {
//        let myVC = storyboard?.instantiateViewController(withIdentifier: "goalsAdd") as! GoalsAddViewController
//        myVC.userid = passedUserId
//        navigationController?.pushViewController(myVC, animated: true)
//    }
    
    @IBAction func goToAddGoal(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsAdd") as! GoalsAddViewController
        vc.userid = userid!
        vc.player = self.player!
        vc.audiostreaming = self.audiostreaming!
        present(vc, animated: true, completion: nil)
    }
    
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
            print(self.player)
            print("^^^ self.player")
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
    
//    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didChangePlaybackStatus isPlaying: Bool) {
//        print("188")
//        self.player?.queueSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", callback: {(error) in
//            if (error == nil) {
//                print("queued!")
//                self.audiostreaming = audioStreaming
//            } else {
//                print("error queueing")
//            }
//        })
//    }
    
    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didStopPlayingTrack trackUri: String!) {
        print("193")
        print(self.player)
        self.player?.queueSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", callback: {(error) in
            if (error == nil) {
                print("queued!")
                self.player?.playSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", startingWith: 0, startingWithPosition: 0, callback: { (error) in
                    if (error == nil) {
                        print("playing!")
                    }
                    if(error != nil) {
                        print("errors while playing")
                    }
                })
            } else {
                print("error queueing")
            }
        })
    }
    
    @IBAction func pauseSong(){
        print("trying to pause")
        self.player?.setIsPlaying(false, callback: nil)
    }
    
    @IBAction func skip() {
        do {
            try
            print(userid)
            initializaPlayer(authSession:session)
            self.player?.playSpotifyURI("spotify:track:3n3Ppam7vgaVa1iaRUc9Lp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
                if (error == nil) {
                    print("playing!")
                }
                if(error != nil) {
                    print("errors while playing")
                }
            })
        } catch is Error {
            print("ERROR W SKIP")
        }
//        self.player = nil
    }
    
    @IBAction func playSong(){
        print("trying to play")
        self.player?.setIsPlaying(true, callback: nil)
    }
}
