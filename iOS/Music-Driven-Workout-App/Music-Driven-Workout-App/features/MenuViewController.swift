//
//  MenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/23/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class MenuViewController: UIViewController,  SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {

    //var player: SPTAudioStreamingController?
    var userid: String!
    var token: String!
    
    @IBOutlet weak var workout: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        populateUI()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(true)
        workout.isHidden = global.completedWorkout
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    /* Button->Storyboard Navigation */
    @IBAction func goToWorkout(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "workout", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "workoutSelectionID") as! WorkSelectionViewController
//        vc.player = player!
//        vc.token = token!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToSavedWorkouts(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "workout", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "savedWorkoutsID") as! SavedWorkoutsViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToFitnessTest(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "fitnessSelectionID") as! FTSelectionViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToCalibrateExercise(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "calibrateExerciseID") as! CEFilterViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToGoals(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsID") as! GoalsMenuViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToThemes(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToProfile(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "profile", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "profileID") as! ProfileViewController
        present(vc, animated: false, completion: nil)
    }
    @IBAction func goToLogout(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "loginID") as! LoginViewController
        global.reset()
        present(vc, animated: false, completion: nil)
    }
    

    /* END Button->Storyboard Navigation */

    @IBOutlet weak var titletext: UILabel!

    struct usernameResult: Codable {
        var Result: String
        var Status: String
    }

    @objc func populateUI() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/getusername/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + global.userid + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(usernameResult.self, from: data) else { return }
                DispatchQueue.main.async {
                    self.titletext.text = "Welcome back, " + json.Result + "!"
                }
            }

        }.resume()
    }
    
//    @IBAction func logout(_ sender: UIButton) {
//        let userDefaults = UserDefaults.standard
//        if let sessionObj:AnyObject = userDefaults.object(forKey: "SpotifySession") as AnyObject? {
//            sessionObj.logout()
//        }
//    }
}
