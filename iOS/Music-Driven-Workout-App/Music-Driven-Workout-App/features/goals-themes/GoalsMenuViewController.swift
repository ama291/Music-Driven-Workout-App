//
//  GoalsMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class GoalsMenuViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
    
    var userid: String! = "21"
    var goals: [[String:Any]] = []
    var selectedGoal: [String:Any]!
    
    var viewModel = ViewModel()
    var request = APIRequest()
    
    var player: SPTAudioStreamingController?
    var passedUserId = String()
    var auth = SPTAuth.defaultInstance()!
    var audiostreaming: SPTAudioStreamingController?
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        userid = "21"
        
        let qstr = "userid=\(userid!)&key=SoftCon2018"
        request.submitPostLocal(route: "/api/workouts/goalssaved/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            let dataStr = String(data: data!, encoding: .utf8)!
            print(dataStr)
            self.goals += self.request.parseJsonDictList(data: data!)!
            print("GOALSSSSS - ")
            print(self.goals)
            let vmitems = self.goals.map { ViewModelItem(item: Model(title: "\($0["name"]! as! String)" , data: $0)) }
            
            DispatchQueue.main.async {
                self.viewModel.setItems(items: vmitems)
                
                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
                self.tableView?.dataSource = self.viewModel
                self.tableView?.delegate = self.viewModel
                self.tableView?.estimatedRowHeight = 100
                self.tableView?.rowHeight = UITableViewAutomaticDimension
                self.tableView?.allowsSelection = true
                self.tableView?.separatorStyle = .none
            }
        }.resume()
        
        viewModel.didToggleSelection = { [weak self] hasSelection in
            let selected = self!.viewModel.selectedItems
            if selected.count == 0 {
                return
            }
            self!.selectedGoal = self!.viewModel.selectedItems.map{ $0.data}[0]
            self!.performSegue(withIdentifier: "toGoal", sender: nil)
        }
    }

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is GoalViewController
        {
            let vc = segue.destination as? GoalViewController
            //data to send
            vc?.userid = userid
            vc?.selectedGoal = self.selectedGoal
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /* Navigation */
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
 
    
    @IBAction func goToAddGoal(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsAdd") as! GoalsAddViewController
//        vc.player = self.player!
//        vc.audiostreaming = self.audiostreaming!
        present(vc, animated: true, completion: nil)
    }
    
//    @objc func updateAfterFirstLogin () {
//
//        //        loginButton.isHidden = true
//        let userDefaults = UserDefaults.standard
//
//        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
//
//            let sessionDataObj = sessionObj as! Data
//            let firstTimeSession = NSKeyedUnarchiver.unarchiveObject(with: sessionDataObj) as! SPTSession
//
//            self.session = firstTimeSession
//            initializaPlayer(authSession: session)
//            username = session.canonicalUsername
//            token = session.accessToken
//            //            self.loginButton.isHidden = true
//            // self.loadingLabel.isHidden = false
//        }
//    }
    
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
    
//    @IBAction func startMusic(_ sender: UIButton) {
//        print("workoutsummary")
//        print("username")
//        print(username)
//        print("access token")
//        print(token)
//        updateAfterFirstLogin()
//    }
//
//    func initializaPlayer(authSession:SPTSession){
//        if self.player == nil {
//            self.player = SPTAudioStreamingController.sharedInstance()
//            print(self.player)
//            print("^^^ self.player")
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
    
//    func audioStreaming(_ audioStreaming: SPTAudioStreamingController!, didStopPlayingTrack trackUri: String!) {
//        print("193")
//        print(self.player)
//        self.player?.queueSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", callback: {(error) in
//            if (error == nil) {
//                print("queued!")
//                self.player?.playSpotifyURI("spotify:track:6JzzI3YxHCcjZ7MCQS2YS1", startingWith: 0, startingWithPosition: 0, callback: { (error) in
//                    if (error == nil) {
//                        print("playing!")
//                    }
//                    if(error != nil) {
//                        print("errors while playing")
//                    }
//                })
//            } else {
//                print("error queueing")
//            }
//        })
//    }
//
//    @IBAction func pauseSong(){
//        print("trying to pause")
//        self.player?.setIsPlaying(false, callback: nil)
//    }
    
//    @IBAction func skip() {
//        do {
//            try
//            print(userid)
//            initializaPlayer(authSession:session)
//            self.player?.playSpotifyURI("spotify:track:3n3Ppam7vgaVa1iaRUc9Lp", startingWith: 0, startingWithPosition: 0, callback: { (error) in
//                if (error == nil) {
//                    print("playing!")
//                }
//                if(error != nil) {
//                    print("errors while playing")
//                }
//            })
//        } catch is Error {
//            print("ERROR W SKIP")
//        }
////        self.player = nil
//    }
    
//    @IBAction func playSong(){
//        print("trying to play")
//        self.player?.setIsPlaying(true, callback: nil)
//    }
}
