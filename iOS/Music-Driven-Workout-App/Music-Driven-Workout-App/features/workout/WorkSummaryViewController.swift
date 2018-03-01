//
//  WorkSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

<<<<<<< HEAD
class WorkSummaryViewController: UIViewController, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {
=======
class WorkSummaryViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
>>>>>>> d325418e2a7021972821bd9c51b051d927a74daf

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
        print("WorkSummaryVC")
        print("\t userid:" + userid)
        print("\t themes:" + themes)
        print("\t categories:" + categories)
        print("\t musclegroups:" + musclegroup)
        print("\t equipment:" + equipment)
        print("\t duration:" + duration)
        print("\t difficulty:" + difficulty)
        print("\t token:" + token + "\n")
        
        getWorkout()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Mark: Navigation */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSelectionViewController {
            let vc = segue.destination as? WorkSelectionViewController
            vc?.userid = userid!
        }
        else if segue.destination is WorkExerciseViewController {
            let vc = segue.destination as? WorkExerciseViewController
            vc?.userid = userid!
        }
    }
    
    /* Mark: Make a call to getWorkout() */
    var reply: [String:Any] = [String:Any]()
    var exerciseInfo: [String:Any] = [String:Any]()
    var exList: [String] = [String]()
    
    @objc func getWorkout() {
        let request = APIRequest()
        let route = "/api/workouts/getworkout/"
        var query = "userid=" + userid + "&key=SoftCon2018"
        if musclegroup.isEmpty {
            query += "&categories=" + categories
        } else {
            query += "&musclegroups=" + musclegroup
        }
        query += "&equipment=" + equipment
        query += "&duration=" + duration
        query += "&difficulty=" + difficulty
        query += "&token=" + token
        print("QUERY:" + query + "\n")

        request.submitPostLocal(route: route, qstring: query) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            print("initial data:", String(describing: data))
            /* Parse the json object returned by submitPostLocal() */
            let json = try? JSONSerialization.jsonObject(with: data!, options: [])
            print("JSON:", json as Any)
            if let dictionary = json as? [String: Any] {
                if let status = dictionary["Status"] as? String {
                    print("Status:", status)
                }
                
                /* TODO - Turn the Result into a nested dictionary */
                var result = dictionary["Result"] as! String
//                result.remove(at: result.startIndex)
//                result.removeLast()
                print("result: ", result)
                
                //var resultDictionary: [String: [Any]]
                if let resultData = result.data(using: .utf8, allowLossyConversion: false) {
                    do {
                        let reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [String: AnyObject]
                        print("reply JSON:", reply as Any)
                    } catch let error as NSError {
                        print("Failed to Load: \(error.localizedDescription)")
                    }
                }
                
//                if let result = dictionary["Result"] as? String {
//                    print("result", result.data(using: .utf8), result)
//                    let resJson = try? JSONSerialization.jsonObject(with: result.data(using: String.Encoding.utf8)!, options: [])
//                    print("RESJSON: ", resJson as Any)
//                    if let resDict = resJson as? [String: Any] {
//                        if let uid = resDict["uid"] as? String {
//                            print(uid)
//                        } else {print("uid err")}
//                    } else {print("resDict err")}
//                }  else {print("result err")}
                
            }
            
            }.resume()
    }
    
    /* Mark: tableView */
    let sections = ["Exercises"]
    //let exList = ["Test Input 1", "Test Input 2"]
    
    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return sections[section]
    }
    // Number of sections in tableView
    func numberOfSections(in tableView: UITableView) -> Int {
        return sections.count
    }
    // Number of rows in each section of tableView
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        switch section {
        case 0:
            // Exercise Section
            return exList.count
        default:
            return 0
        }
    }
    // Data to fill the tableView with
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Create an object of the dynamic cell "PlainCell"
        let cell = tableView.dequeueReusableCell(withIdentifier: "PlainCell", for: indexPath)
        
        // Depending on the section, fill the textLabel with the relevant text
        switch indexPath.section {
        case 0:
            cell.textLabel?.text = exList[indexPath.row]
            break
        default:
            break
        }
    
        // Return the configured cell
        return cell
    }
<<<<<<< HEAD
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
=======
>>>>>>> d325418e2a7021972821bd9c51b051d927a74daf

}
