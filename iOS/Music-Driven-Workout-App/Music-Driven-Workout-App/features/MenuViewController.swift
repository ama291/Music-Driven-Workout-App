//
//  MenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/23/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class MenuViewController: UIViewController {
    
    var userid: String!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        populateUI()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Segue Navigation */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSelectionViewController {
            let vc = segue.destination as? WorkSelectionViewController
            //data to send
            vc?.userid = userid!
        }
    }
    
    /* Button->Storyboard Navigation */
    @IBAction func goToWorkout(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "workout", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "workoutSelectionID") as! WorkSelectionViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToSavedWorkouts(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "workout", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "savedWorkoutsID") as! SavedWorkoutsViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToFitnessTest(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "fitnessSelectionID") as! FTSelectionViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToCalibrateExercise(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "calibrateExerciseID") as! CEFilterViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToGoals(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "goalsTable") as! GoalsMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToThemes(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToProfile(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "profile", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "profileID") as! ProfileViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
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
        let postString = "userid=" + userid + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(usernameResult.self, from: data) else { return }
                print(json)
                DispatchQueue.main.async {
                    self.titletext.text = "Welcome back, " + json.Result + "!"
                }
            }
            
        }.resume()
    }
}
