//
//  GoalsMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//
import UIKit

class ThemesMenuViewController: UIViewController {
    
    var tableArray = [String:Any] ()
    var token = global.token!
    var passedUserId = String()
    //var userid: String! = "21"
    var themes: [[String:Any]] = []
    var selectedTheme: [String:Any]!

    
    var viewModel = ViewModel()
    var request = APIRequest()
    
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
//        self.tableView.dataSource = self
//        self.tableView.delegate = self
//        // Do any additional setup after loading the view.
//        populateThemes()
        self.tableView.reloadData()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        //        recuperaEmpresas()
        //        userid = "21"
        //        self.themes = [["theme":"theme", "name": "theme name", "spotifyId": "Spotify id", "numworkouts": "4"], ["theme":"theme 2", "name": "theme name 2", "spotifyId": "Spotify id 2", "numworkouts": "6"]]
        
        let qstr = "userid=\(global.userid!)&key=SoftCon2018"
        request.submitPostServer(route: "/api/workouts/themessaved/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            let dataStr = String(data: data!, encoding: .utf8)!
            print(dataStr)
            self.themes += self.request.parseJsonDictList(data: data!)!
            print("THEMES")
            print(self.themes)
            let vmitems = self.themes.map { ViewModelItem(item: Model(title: "\($0["name"]! as! String)" , data: $0)) }
            
            
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
            self!.selectedTheme = self!.viewModel.selectedItems.map{ $0.data}[0]
            self!.performSegue(withIdentifier: "toTheme", sender: nil)
        }
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /* Navigation */
    
//    struct themesResult: Codable {
//        var Result: String
//        var Status: String
//    }
//
//    func populateThemes() {
//        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/themessaved/") else { return }
//        var request = URLRequest(url: url)
//        request.httpMethod = "POST"
//        let postString = "userid=" + global.userid + "&key=SoftCon2018"
//        passedUserId = global.userid
//        request.httpBody = postString.data(using: String.Encoding.utf8)
//        let session = URLSession.shared
//        session.dataTask(with: request) { (data, response, error) in
//            guard let content = data else {
//                print("not returning data")
//                return
//            }
//            guard let json = (try? JSONSerialization.jsonObject(with: content, options: JSONSerialization.ReadingOptions.mutableContainers)) as? [String: Any] else {
//                print("Not containing JSON")
//                return
//            }
//
//            if let array = json as? [String: Any] {
//                self.tableArray = array
//                print(self.tableArray)
//            }
//
//            print(self.tableArray)
//            DispatchQueue.main.async {
//                self.tableView.reloadData()
//            }
//            }.resume()
//    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is ThemeViewController
        {
            let vc = segue.destination as? ThemeViewController
            //data to send
            vc?.selectedTheme = self.selectedTheme
        }
    }
    
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
    
//    @IBAction func goToAddTheme(_ sender: UIButton) {
//        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
//        let vc = storyboard.instantiateViewController(withIdentifier: "themesAdd") as! ThemesAddViewController
//        vc.userid = userid!
//        vc.token = token!
//        present(vc, animated: true, completion: nil)
//    }
//
//    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
//        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath) as UITableViewCell
//        cell.textLabel?.text = (self.tableArray["Result"]! as! String)
//
//        return cell
//    }
//
//    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
//        return self.tableArray.count/2
//    }
    
}
