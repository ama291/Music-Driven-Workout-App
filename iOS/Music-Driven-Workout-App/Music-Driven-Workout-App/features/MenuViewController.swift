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
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
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
        let vc = storyboard.instantiateViewController(withIdentifier: "workoutSelectionID") as UIViewController
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToSavedWorkouts(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "workout", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "savedWorkoutsID") as UIViewController
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToFitnessTest(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "fitnessSelectionID") as UIViewController
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToCalibrateExercise(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "fitness-calibration", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "calibrateExerciseID") as UIViewController
        present(vc, animated: true, completion: nil)
    }
    @IBAction func goToGoals(_ sender: UIButton) {
    }
    @IBAction func goToThemes(_ sender: UIButton) {
    }
    @IBAction func goToProfile(_ sender: UIButton) {
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
